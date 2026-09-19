# -*- coding: utf-8 -*-
"""llm_client.py v2 — 统一 LLM 客户端（仅 DeepSeek 付费 API）

模型选型（"合适的"原则）:
  - deepseek-v4-flash : 默认, 快速便宜, 批量分析/抽取够用
  - deepseek-chat     : 分类/对话类任务用 Chat 更合适
  - 不使用 deepseek-v4-pro（贵）, 不使用 OpenRouter / NVIDIA NIM 等免费模型

仅走付费 DeepSeek API (https://api.deepseek.com); 失败返回 None 由调用方处理, 不降级免费端点。
Key 来源: ~/.dsh/.credentials.yaml (与 DSH harness 同源) 或环境变量
"""
import json, os, re, time, random, urllib.request, urllib.error
from pathlib import Path

PRIMARY_MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-flash")
BASE_URL = "https://api.deepseek.com"


def _load_key():
    """从 ~/.dsh/.credentials.yaml 读取 DEEPSEEK_API_KEY"""
    env = os.environ.get("DEEPSEEK_API_KEY")
    if env:
        return env
    cred = Path.home() / ".dsh" / ".credentials.yaml"
    if cred.exists():
        m = re.search(r"DEEPSEEK_API_KEY:\s*(\S+)", cred.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return ""


def _post(url, payload, headers, timeout=90):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")[:200]
        print(f"  [llm_client] HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"  [llm_client] {type(e).__name__}: {e}")
        return None


def call(prompt, max_tokens=1500, timeout=90, model=None, retries=3, total_timeout=None):
    """调用 LLM（仅 DeepSeek 付费 API）。返回文本或 None。带重试(限速/网络波动)。

    total_timeout: 整个调用(含重试+退避)的墙钟上限秒数; 不传则按 retries*timeout+20 兜底,
    防止单次调用因端点挂起而无限累加 timeout。
    """
    chosen = model or PRIMARY_MODEL
    key = _load_key()
    if total_timeout is None:
        total_timeout = timeout * (retries + 1) + 20
    deadline = time.time() + total_timeout

    def attempt():
        # 仅 DeepSeek 付费 API（不回落免费端点）
        if not key:
            return None
        # 单次调用超时也掐到剩余墙钟, 使 total_timeout 成为硬上限(防挂起)
        remaining = max(1.0, deadline - time.time())
        return _post(
            f"{BASE_URL}/v1/chat/completions",
            {"model": chosen, "messages": [{"role": "user", "content": prompt}],
             "max_tokens": max_tokens, "temperature": 0.3},
            {"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
            timeout=min(timeout, remaining),
        )

    for i in range(retries + 1):
        if time.time() > deadline:
            print(f"  [llm_client] 总超时({total_timeout:.0f}s), 放弃剩余重试")
            return None
        r = attempt()
        if r:
            return r
        if i < retries:
            remaining = deadline - time.time()
            sleep_t = min((2 ** i) + random.uniform(0, 1), max(0.5, remaining))
            if sleep_t > 0:
                time.sleep(sleep_t)
    return None


def call_json(prompt, max_tokens=1500, timeout=90, model=None, total_timeout=None):
    """调用 LLM 并解析 JSON 返回 dict。失败返回 None。"""
    r = call(prompt, max_tokens=max_tokens, timeout=timeout, model=model, total_timeout=total_timeout)
    if not r:
        return None
    m = re.search(r'\{.*\}', r, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass
    return {"raw": r}


if __name__ == "__main__":
    test = call_json('请回复JSON: {"ok": true, "msg": "LLM可用"}')
    print(f"LLM test: {test}")
