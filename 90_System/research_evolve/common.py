# -*- coding: utf-8 -*-
"""research_evolve.common — 共享工具层。

设计约束（对照 AGENTS.md 零、1.2、1.4）：
  * 只用标准库 + pyyaml（本机 Python 3.10 已具备），不引入新依赖。
  * 所有状态写入走原子替换，避免历史发生过的"中断写坏状态文件"。
  * 不杜撰数字：本包产出的每个计数都来自实际扫描，且记录扫描口径。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path

try:  # Windows 控制台/重定向编码保护
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------- 路径
VAULT = Path(r"D:\Obsidian\vault")
PKG = VAULT / "90_System" / "research_evolve"
STATE_DIR = PKG / "state"
REGISTRY_FILE = STATE_DIR / "registry.json"
PAPERS_FILE = PKG / "papers.yaml"
FRAMEWORK_FILE = PKG / "framework_manifest.yaml"
CONFIG_FILE = PKG / "config.yaml"
REPORT_FILE = VAULT / "70_Dashboard" / "research_evolve.md"
RUN_LOG_FILE = VAULT / "99_Meta" / "research_evolve_log.json"
CODEX_DIR = Path(r"D:\Obsidian\.codex")
KEYWORDS_FILE = CODEX_DIR / "research_keywords.yaml"

# 证据标签：与 AGENTS.md / research_agent_contract.yaml 保持一致
EVIDENCE_LABELS = ("[实测]", "[仿真]", "[引用]", "[推导]", "[假设]", "[待测]", "[综合]")

# 候选生命周期状态（selection memory 的核心枚举）
VERDICTS = ("open", "accepted", "rejected", "deferred", "adopted", "done", "superseded")
CLOSED_VERDICTS = ("rejected", "deferred", "adopted", "done", "superseded")

# 候选种类
KINDS = ("hypothesis", "idea", "bridge", "evolution_item", "concept_debt", "gate_finding")


# ---------------------------------------------------------------- 日志
class RunLog:
    """一次运行的日志缓冲，同时打印并最终落盘。"""

    def __init__(self, name: str):
        self.name = name
        self.entries: list[tuple[str, str]] = []
        self.t0 = datetime.now()

    def __call__(self, msg: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self.entries.append((datetime.now().isoformat(), msg))
        print(f"[{self.name}] {msg}", flush=True)

    def as_dict(self) -> dict:
        return {
            "step": self.name,
            "started": self.t0.isoformat(),
            "seconds": round((datetime.now() - self.t0).total_seconds(), 1),
            "entries": self.entries,
        }


def append_run_log(records: list[dict], keep: int = 40) -> None:
    """把本轮各步骤日志追加到 99_Meta/research_evolve_log.json（保留最近 keep 轮）。"""
    history: list = []
    if RUN_LOG_FILE.exists():
        try:
            history = json.loads(RUN_LOG_FILE.read_text(encoding="utf-8"))
            if not isinstance(history, list):
                history = []
        except Exception:
            history = []
    history.append({"date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().isoformat(),
                    "steps": records})
    save_json(RUN_LOG_FILE, history[-keep:])


# ---------------------------------------------------------------- 原子 I/O
def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except Exception:
            pass
        raise


def save_json(path: Path, obj) -> None:
    _atomic_write(path, json.dumps(obj, ensure_ascii=False, indent=2))


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def load_yaml(path: Path, default=None):
    """读 YAML；缺 pyyaml 或解析失败时返回 default 而不是抛异常（失败隔离）。"""
    if not path.exists():
        return default
    try:
        import yaml  # noqa: PLC0415
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_yaml(path: Path, obj) -> None:
    import yaml  # noqa: PLC0415
    _atomic_write(path, yaml.safe_dump(obj, allow_unicode=True, sort_keys=False,
                                       default_flow_style=False))


# ---------------------------------------------------------------- 规范化 / 去重
_WS_RE = re.compile(r"[\s\u3000]+")
_PUNCT_RE = re.compile(r"[，。；：、！？（）【】《》\"'`·\-—_/\\|,.!?;:()\[\]{}<>~^*#]+")


def norm_title(text: str) -> str:
    """把标题规范化为去重键：全角转半角、去标点空白、小写。

    这是 selection memory 的关键——同一想法换一种写法必须命中同一条记忆，
    否则"否决"永远拦不住复现（当前系统的实际故障）。
    """
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", str(text)).lower()
    t = _PUNCT_RE.sub(" ", t)
    t = _WS_RE.sub(" ", t).strip()
    return t


def dedup_key(kind: str, title: str) -> str:
    """候选去重键 = 种类 + 规范化标题的 sha1 前 16 位。"""
    return hashlib.sha1(f"{kind}::{norm_title(title)}".encode("utf-8")).hexdigest()[:16]


def text_hash(text: str) -> str:
    return hashlib.sha1((text or "").encode("utf-8")).hexdigest()


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def days_between(iso_a: str, iso_b: str | None = None) -> float:
    """返回 iso_a 到 iso_b（默认现在）的天数；解析失败返回 0。"""
    try:
        a = datetime.fromisoformat(iso_a)
    except Exception:
        return 0.0
    b = datetime.fromisoformat(iso_b) if iso_b else datetime.now()
    try:
        return (b - a).total_seconds() / 86400.0
    except Exception:
        return 0.0


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


# ---------------------------------------------------------------- wiki 链接解析
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")


def wikilinks(text: str) -> list[str]:
    """提取 [[目标]] 的目标名（去别名与锚点）。"""
    out = []
    for m in WIKILINK_RE.findall(text or ""):
        t = m.strip().replace("\\", "").strip()
        if t:
            out.append(t)
    return out


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """轻量 frontmatter 解析（不依赖 yaml），返回 (字段dict, 正文)。"""
    m = FRONTMATTER_RE.match(text or "")
    if not m:
        return {}, text or ""
    fm_raw, body = m.group(1), text[m.end():]
    fm: dict = {}
    for line in fm_raw.splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key:
            fm[key] = val
    return fm, body


# ---------------------------------------------------------------- 框架词表
def load_vocabulary() -> dict:
    """加载 .codex/research_keywords.yaml；这是唯一词表真相源（不在此重复定义）。"""
    data = load_yaml(KEYWORDS_FILE, default=None)
    if not isinstance(data, dict):
        return {"tcc": [], "inest": [], "exclusions": [], "loaded": False}
    tcc: list[str] = []
    inest: list[str] = []
    for section in ("identity", "core", "architecture"):
        tcc += [str(x) for x in (data.get("tcc", {}) or {}).get(section, []) or []]
    for section in ("identity", "dynamics", "substrate", "theory"):
        inest += [str(x) for x in (data.get("inest", {}) or {}).get(section, []) or []]
    excl = [str(x) for x in data.get("exclusions", []) or []]
    return {"tcc": tcc, "inest": inest, "exclusions": excl, "loaded": True}


def load_config() -> dict:
    """读取本包阈值配置，缺项用内置安全默认值补齐。"""
    defaults = {
        "max_human_decisions": 7,        # 每次呈现给用户的决策条数上限
        "max_open_days": 14,             # 未裁决候选的年龄上限，超过则升级
        "defer_min_seen": 3,             # 反复出现却始终不可执行的阈值
        "freeze_requires_new_source": True,   # 无新来源时冻结新增概念
        "gate_paths": ["50_Output/51_Papers", "50_Output/52_Patents", "50_Output/53_Monographs"],
        "gate_scan_limit": 400,          # 单次扫描文件上限，防超时
        "min_accept_score": 0.55,        # 自动建议"采纳"的分数门槛
        "weights": {
            "framework_fit": 0.34,
            "testability": 0.28,
            "evidence_ready": 0.22,
            "bridge_value": 0.16,
        },
    }
    cfg = load_yaml(CONFIG_FILE, default=None)
    if not isinstance(cfg, dict):
        return defaults
    for k, v in defaults.items():
        cfg.setdefault(k, v)
    if isinstance(cfg.get("weights"), dict):
        for k, v in defaults["weights"].items():
            cfg["weights"].setdefault(k, v)
    else:
        cfg["weights"] = defaults["weights"]
    return cfg
