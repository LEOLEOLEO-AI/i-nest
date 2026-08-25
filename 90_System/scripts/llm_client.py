# -*- coding: utf-8 -*-
"""llm_client.py — 统一 LLM 客户端（多级回退）"""
import json, os, urllib.request

def _post(url, payload, headers, timeout=60):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"  [llm_client] {url.split('/')[2]} err: {type(e).__name__}")
        return None

def _get_key(name):
    return os.environ.get(name, "")

def call(prompt, max_tokens=1000, timeout=60):
    """NVIDIA NIM(免费 DeepSeek) -> 本地代理, 返回文本或 None"""
    key = _get_key("NVIDIA_API_KEY")
    if key:
        for model in ("deepseek-ai/deepseek-v4-flash-0731",
                      "deepseek-ai/deepseek-coder-6.7b-instruct"):
            r = _post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                {"model": model, "messages": [{"role": "user", "content": prompt}],
                 "max_tokens": max_tokens, "temperature": 0.3},
                {"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
                timeout=timeout,
            )
            if r:
                return r
    r = _post(
        os.environ.get("LLM_BASE_URL", "http://127.0.0.1:10100") + "/v1/chat/completions",
        {"model": os.environ.get("LLM_MODEL", "deepseek-v4-pro"),
         "messages": [{"role": "user", "content": prompt}],
         "max_tokens": max_tokens, "temperature": 0.3},
        {"Content-Type": "application/json", "Authorization": "Bearer sk-local"},
        timeout=timeout,
    )
    return r

if __name__ == "__main__":
    r = call("回复OK")
    print(f"LLM test: {r!r}")
