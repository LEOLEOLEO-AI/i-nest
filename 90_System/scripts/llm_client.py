# -*- coding: utf-8 -*-
"""llm_client.py v2 — 统一 LLM 客户端（DeepSeek 直连主力）

模型: deepseek-v4-flash (快速便宜, 批量分析够用)
       deepseek-v4-pro   (复杂任务手动切换)

回退链: DeepSeek API -> NVIDIA NIM -> 全部失败返回 None(调用方报错, 不降级规则)
Key 来源: ~/.dsh/.credentials.yaml (与 DSH harness 同源) 或环境变量
"""
import json, os, re, urllib.request, urllib.error
from pathlib import Path

PRIMARY_MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-flash")
PRO_MODEL = "deepseek-v4-pro"
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


def call(prompt, max_tokens=1500, timeout=90, model=None, retries=3):
    """调用 LLM。返回文本或 None。带重试(限速/网络波动)。"""
    chosen = model or PRIMARY_MODEL
    key = _load_key()

    def attempt():
        # 1) DeepSeek 直连（主力）
        if key:
            r = _post(
                f"{BASE_URL}/v1/chat/completions",
                {"model": chosen, "messages": [{"role": "user", "content": prompt}],
                 "max_tokens": max_tokens, "temperature": 0.3},
                {"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
                timeout=timeout,
            )
            if r:
                return r
        # 2) NVIDIA NIM 免费（备用, 网络可达时）
        nv = os.environ.get("NVIDIA_API_KEY", "")
        if nv:
            r = _post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                {"model": "deepseek-ai/deepseek-v4-flash-0731",
                 "messages": [{"role": "user", "content": prompt}],
                 "max_tokens": max_tokens, "temperature": 0.3},
                {"Content-Type": "application/json", "Authorization": f"Bearer {nv}"},
                timeout=timeout,
            )
            if r:
                return r
        return None

    import time, random
    for i in range(retries + 1):
        r = attempt()
        if r:
            return r
        if i < retries:
            # 指数退避 + 抖动：~2s, 4s, 8s（DeepSeek 间歇性连接拒绝/超时时更稳健）
            time.sleep((2 ** i) + random.uniform(0, 1))
    return None


def call_json(prompt, max_tokens=1500, timeout=90, model=None):
    """调用 LLM 并解析 JSON 返回 dict。失败返回 None。"""
    r = call(prompt, max_tokens=max_tokens, timeout=timeout, model=model)
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
