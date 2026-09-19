# -*- coding: utf-8 -*-
"""sim_platform.harness — 可复现运行器 + 实验注册表（治理"版本蔓延"）。

实测问题（2026-09-19）:
    40_iNEST/45_Simulation/sdi_sim 下同一个实验有
    sdi_experiment1_{v2…v19, v12b, v12c, v17b, final, universal} —— **24 个版本并存**。
    这违反 AGENTS.md 的"可复现"要求：
      * 说不清哪个是当前有效版本；
      * 无法判断某次结论出自哪个版本；
      * 目录里堆着 24 个近似文件，后来者无从下手。

本模块给两件事:
    1. **实验注册表**（exp_registry.json）：一个实验**只有一个规范脚本**，
       历史版本由 git 承载，注册表只记录"版本事件"（谁、何时、为什么改）。
    2. **可复现运行**：每次运行写 run_manifest.json —— 种子、配置哈希、
       依赖版本、git 提交、结果哈希 —— 让任何结论都能被追溯与重跑。

证据等级: 所有产物标 [仿真]。
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

SIM = Path(r"D:\Obsidian\vault\40_iNEST\45_Simulation")
VAULT = Path(r"D:\Obsidian\vault")
# 代码放 90_System（工具层），产物放 40_iNEST/45_Simulation（研究数据层）——
# 与 vault 的既定分工一致：90_System 是工具，30/40 是研究实体。
PLATFORM_CODE = VAULT / "90_System" / "sim_platform"
EXPERIMENTS = PLATFORM_CODE / "experiments"
ARTIFACTS = SIM / "sim_platform"
RUNS = ARTIFACTS / "runs"
REGISTRY = ARTIFACTS / "exp_registry.json"

EVIDENCE = "[仿真]"


# ---------------------------------------------------------------- 工具
def _hash(obj) -> str:
    s = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def _deps() -> dict:
    out = {}
    for m in ("numpy", "scipy", "networkx", "brian2", "pandas", "matplotlib"):
        try:
            mod = __import__(m)
            out[m] = getattr(mod, "__version__", "?")
        except Exception:
            pass
    return out


def _git_commit() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(VAULT),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="ignore", timeout=20)
        return (r.stdout or "").strip() or "?"
    except Exception:
        return "?"


# ---------------------------------------------------------------- 注册表
def load_registry() -> dict:
    if REGISTRY.exists():
        try:
            return json.loads(REGISTRY.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"schema": "sim-platform-registry-v1", "experiments": {}}


def save_registry(reg: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    reg["updated"] = datetime.now().isoformat()
    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")


def register(exp_id: str, title: str, workstream: str = "SIM",
             canonical_script: str | None = None, note: str = "") -> dict:
    """登记一个实验（幂等）。一个实验只允许一个规范脚本。"""
    reg = load_registry()
    exps = reg.setdefault("experiments", {})
    rec = exps.get(exp_id)
    if rec is None:
        rec = {
            "id": exp_id, "title": title, "workstream": workstream,
            "canonical_script": canonical_script or f"sim_platform/experiments/{exp_id}.py",
            "created": datetime.now().isoformat(),
            "versions": [{"v": 1, "at": datetime.now().isoformat(), "note": note or "初始登记"}],
            "runs": [],
        }
        exps[exp_id] = rec
    elif note:
        v = len(rec.get("versions", [])) + 1
        rec.setdefault("versions", []).append(
            {"v": v, "at": datetime.now().isoformat(), "note": note})
    save_registry(reg)
    return rec


def record_run(exp_id: str, run_id: str, manifest: dict) -> None:
    reg = load_registry()
    rec = reg.setdefault("experiments", {}).setdefault(
        exp_id, {"id": exp_id, "title": exp_id, "versions": [], "runs": []})
    rec.setdefault("runs", []).append({
        "run_id": run_id, "at": manifest.get("finished"),
        "seed": manifest.get("seed"), "config_hash": manifest.get("config_hash"),
        "result_hash": manifest.get("result_hash"),
        "manifest": str((RUNS / exp_id / run_id / "run_manifest.json").relative_to(SIM)),
        "evidence": EVIDENCE})
    rec["runs"] = rec["runs"][-200:]
    save_registry(reg)


# ---------------------------------------------------------------- 版本蔓延体检
import re as _re
VERSION_PAT = _re.compile(r"(_v\d+[a-z]?|_final\d*|_universal|_revised|_new)$")


def lint_version_sprawl(roots: list[Path] | None = None, min_group: int = 4) -> list[dict]:
    """扫描"同一实验的多版本并存"，直接对应实测到的 24 版本问题。"""
    roots = roots or [SIM, VAULT / "30_TCC" / "35_Simulation"]
    groups: dict[str, list[str]] = {}
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.py"):
            if "sim_platform" in p.parts or "_vendor" in p.parts:
                continue
            stem = p.stem
            base = VERSION_PAT.sub("", stem)
            if base != stem:
                groups.setdefault(f"{root.name}/{base}", []).append(
                    p.relative_to(root).as_posix())
    return [{"group": k, "count": len(v), "files": sorted(v)}
            for k, v in sorted(groups.items(), key=lambda x: -len(x[1]))
            if len(v) >= min_group]


# ---------------------------------------------------------------- 运行
@dataclass
class RunResult:
    run_id: str
    manifest: dict
    results: dict
    out_dir: Path


def run(exp_id: str, fn, config: dict, seed: int = 0,
        title: str = "", workstream: str = "SIM") -> RunResult:
    """执行一次实验，落盘 manifest + results + report。

    fn(config, seed) -> dict（必须是**纯函数式**的：给定 config+seed 可复现）
    """
    register(exp_id, title or exp_id, workstream)
    if not EXPERIMENTS.exists():
        EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + f"-s{seed}"
    out = RUNS / exp_id / run_id
    out.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    try:
        results = fn(config, seed)
        status = "ok"
        err = ""
    except Exception as e:
        results = {}
        status = "error"
        err = f"{type(e).__name__}: {e}"

    manifest = {
        "experiment": exp_id, "run_id": run_id, "title": title or exp_id,
        "workstream": workstream, "evidence": EVIDENCE,
        "status": status, "error": err,
        "started": datetime.now().isoformat(),
        "seconds": round(time.time() - t0, 2),
        "seed": seed, "config": config, "config_hash": _hash(config),
        "result_hash": _hash(results) if status == "ok" else "",
        "python": sys.version.split()[0], "platform": platform.platform(),
        "dependencies": _deps(), "git_commit": _git_commit(),
        "finished": datetime.now().isoformat(),
    }
    (out / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    # 人读报告
    L = [f"# 仿真报告 · {manifest['title']}", "",
         f"- 实验 `{exp_id}` · 运行 `{run_id}`", f"- 证据等级 **{EVIDENCE}**",
         f"- 状态 **{status}**" + (f"（{err}）" if err else ""),
         f"- 随机种子 `{seed}` · 配置哈希 `{manifest['config_hash']}` · "
         f"结果哈希 `{manifest['result_hash']}`",
         f"- git `{manifest['git_commit']}` · Python {manifest['python']}",
         f"- 耗时 {manifest['seconds']}s", "",
         "## 配置", "", "```json",
         json.dumps(config, ensure_ascii=False, indent=2), "```", "",
         "## 结果", "", "```json",
         json.dumps(results, ensure_ascii=False, indent=2, default=str)[:6000], "```", "",
         "## 复现命令", "", "```bash",
         f'cd D:\\Obsidian\\vault\\90_System && python -m sim_platform.run {exp_id} '
         f'--seed {seed}', "```", "",
         f"> 所有数值均为 **{EVIDENCE}**，不构成实测结论（AGENTS.md §0.1）。"]
    (out / "report.md").write_text("\n".join(L), encoding="utf-8")

    record_run(exp_id, run_id, manifest)
    return RunResult(run_id, manifest, results, out)
