#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vision_analyze.py — 图像分析工具 (deepseek-v4-flash-vision-exp)

用法:
  python vision_analyze.py <图片路径> ["问题文本，默认: 请详细描述这张图并提取关键信息"]
  python vision_analyze.py --list          # 列出近期可分析的图(50_Output/figs等)

输出写入: 99_Meta/vision_analysis/ 或 stdout
"""
import base64, json, os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import llm_client

VAULT = Path(r"D:\Obsidian\vault")
VISION_MODEL = "deepseek-v4-flash-vision-exp"
BASE_URL = "https://api.deepseek.com"
SUPPORTED = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".webp": "image/webp", ".gif": "image/gif"}


def _load_key():
    env = os.environ.get("DEEPSEEK_API_KEY")
    if env:
        return env
    cred = Path.home() / ".dsh" / ".credentials.yaml"
    if cred.exists():
        m = re.search(r"DEEPSEEK_API_KEY:\s*(\S+)", cred.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return ""


def analyze_image(image_path, question):
    import urllib.request, urllib.error
    img = Path(image_path)
    ext = img.suffix.lower()
    if ext not in SUPPORTED:
        print(f"不支持格式 {ext}，支持: {list(SUPPORTED.keys())}")
        return None
    mime = SUPPORTED[ext]
    if img.stat().st_size > 20 * 1024 * 1024:
        print("图片超过 20MB 限制")
        return None
    b64 = base64.b64encode(img.read_bytes()).decode("ascii")

    payload = {
        "model": VISION_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ],
        }],
        "max_tokens": 1500,
        "temperature": 0.2,
    }
    key = _load_key()
    req = urllib.request.Request(
        f"{BASE_URL}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"].strip()
        reasoning = data["choices"][0]["message"].get("reasoning_content", "")
        result = {"image": str(img), "question": question, "answer": content,
                  "reasoning": reasoning[:2000]}
        out_dir = VAULT / "99_Meta" / "vision_analysis"
        out_dir.mkdir(parents=True, exist_ok=True)
        qtag = re.sub(r"[^\w]", "_", (question[:10] or "desc"))
        outfile = out_dir / f"{img.stem[:40]}_{qtag}.json"
        outfile.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[vision] 分析完成 -> {outfile}")
        print(f"  回答: {content[:500]}")
        return result
    except urllib.error.HTTPError as e:
        print(f"[vision] HTTP {e.code}: {e.read().decode('utf-8','ignore')[:200]}")
        return None
    except Exception as e:
        print(f"[vision] 失败: {e}")
        return None


def list_images():
    dirs = [
        VAULT / "50_Output", VAULT / "40_iNEST" / "45_Simulation",
        VAULT / "30_TCC" / "35_Simulation", VAULT / "figures",
        VAULT / "assets",
    ]
    found = []
    for d in dirs:
        if d.exists():
            for ext in SUPPORTED:
                found.extend(d.rglob(f"*{ext}"))
    found.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    print(f"找到 {len(found)} 张图片（最近 15 张）:")
    for f in found[:15]:
        print(f"  {f} ({round(f.stat().st_size/1024)}KB, {f.stat().st_mtime:>10.0f})")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--list":
        list_images()
        sys.exit(0)
    img_path = args[0]
    question = args[1] if len(args) > 1 else "请详细描述这张图的内容，提取所有关键信息（标题、坐标轴、趋势、数值、结构）。"
    analyze_image(img_path, question)
