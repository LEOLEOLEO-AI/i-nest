from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
import streamlit as st
from bs4 import BeautifulSoup


KB_ROOT = Path(r"D:\\Obsidian\\Agent\01-Theory-Research")
INBOX_WEB = KB_ROOT / "Inbox" / "web"
CONFIG_PATH = KB_ROOT / "knowledge_base_config.json"
STATE_PATH = KB_ROOT / "Logs" / "knowledge_base_ingest_state.json"
INGEST_SCRIPT = Path(r"D:\\Obsidian\\Agent\scripts\knowledge_base_ingest.py")


st.set_page_config(page_title="Knowledge Link Import", page_icon="📚", layout="wide")


def ensure_dirs() -> None:
    for path in (INBOX_WEB, KB_ROOT / "Logs"):
        path.mkdir(parents=True, exist_ok=True)


def safe_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", name).strip("_")
    return cleaned or "imported_item"


def ensure_unique_file_path(path: Path) -> Path:
    if not path.exists():
        return path
    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("请输入有效的 http/https 链接")


def infer_title_from_html(html_text: str, fallback: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        if title:
            return title
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        return og_title["content"].strip()
    h1 = soup.find("h1")
    if h1:
        text = h1.get_text(" ", strip=True)
        if text:
            return text
    return fallback


def visible_text_from_html(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def looks_like_shell_page(html_text: str) -> bool:
    lower = html_text.lower()
    visible_text = visible_text_from_html(html_text)
    shell_markers = [
        '<div id="app"></div>',
        '<div id="root"></div>',
        '<div id="protal-root"></div>',
        "window.__initial_state__= {}",
        "window.__initial_state__ = {}",
        "you need to enable javascript to run this app.",
    ]
    marker_hit = any(marker in lower for marker in shell_markers)
    very_short_visible_text = len(visible_text) < 120
    return marker_hit and (
        very_short_visible_text
        or visible_text.lower() == "you need to enable javascript to run this app."
    )


def fallback_name_from_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.netloc or "link").split(":")[0]
    path_name = Path(parsed.path).stem
    if path_name and path_name.lower() not in {"default", "index", "home"}:
        return path_name
    return host.replace(".", "_")


def extension_from_response(url: str, response: requests.Response) -> str:
    parsed = urlparse(url)
    path_ext = Path(parsed.path).suffix.lower()
    if path_ext in {".pdf", ".html", ".htm", ".docx", ".txt", ".md"}:
        return path_ext
    content_type = (response.headers.get("Content-Type") or "").lower()
    if "pdf" in content_type:
        return ".pdf"
    if "wordprocessingml" in content_type or "docx" in content_type:
        return ".docx"
    if "text/plain" in content_type:
        return ".txt"
    return ".html"


def fetch_and_store(url: str) -> Path:
    validate_url(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    today_dir = INBOX_WEB / datetime.now().strftime("%Y%m%d")
    today_dir.mkdir(parents=True, exist_ok=True)

    ext = extension_from_response(url, response)
    fallback = fallback_name_from_url(url)

    if ext in {".html", ".htm"}:
        response.encoding = response.encoding or response.apparent_encoding or "utf-8"
        content = response.text
        if looks_like_shell_page(content):
            raise ValueError("抓取到的是动态壳页面，未包含正文内容；当前链接无法直接导入，请改用可公开访问的正文页或导出文件。")
        title = infer_title_from_html(content, fallback)
        target = today_dir / f"{safe_name(title)}.html"
        counter = 2
        while target.exists():
            target = today_dir / f"{safe_name(title)}_{counter}.html"
            counter += 1
        target.write_text(content, encoding="utf-8")
        return target

    target = today_dir / f"{safe_name(fallback)}{ext}"
    counter = 2
    while target.exists():
        target = today_dir / f"{safe_name(fallback)}_{counter}{ext}"
        counter += 1
    target.write_bytes(response.content)
    return target


def store_local_file(file_path: Path) -> Path:
    if not file_path.exists() or not file_path.is_file():
        raise ValueError(f"本地文件不存在: {file_path}")
    today_dir = INBOX_WEB / datetime.now().strftime("%Y%m%d")
    today_dir.mkdir(parents=True, exist_ok=True)
    target = ensure_unique_file_path(today_dir / file_path.name)
    shutil.copy2(file_path, target)
    return target


def store_uploaded_file(uploaded_file) -> Path:
    today_dir = INBOX_WEB / datetime.now().strftime("%Y%m%d")
    today_dir.mkdir(parents=True, exist_ok=True)
    original_name = Path(uploaded_file.name).name or "uploaded_file"
    target = ensure_unique_file_path(today_dir / original_name)
    target.write_bytes(uploaded_file.getbuffer())
    return target


def run_ingest() -> tuple[int, str, str]:
    command = [
        "python",
        str(INGEST_SCRIPT),
        "--config",
        str(CONFIG_PATH),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    return completed.returncode, completed.stdout, completed.stderr


def read_recent_imports(limit: int = 20) -> list[dict]:
    if not STATE_PATH.exists():
        return []
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    items = list((data.get("items") or {}).values())
    items.sort(key=lambda item: item.get("imported_at", ""), reverse=True)
    return items[:limit]


ensure_dirs()

st.title("本地知识库统一导入 MVP")
st.caption("粘贴任意公开链接，自动抓取并导入到本地知识库，不区分来源。")

col1, col2 = st.columns([2, 1])
with col1:
    url_input = st.text_area(
        "链接地址或本地文件路径",
        height=140,
        placeholder="每行一个链接或本地文件路径，例如：\nhttps://example.com/article\nhttps://mp.weixin.qq.com/s/xxxx\nD:\\export\\getnote_article.html\nD:\\export\\wechat_note.pdf",
    )
with col2:
    auto_ingest = st.checkbox("下载后立即入库", value=True)
    show_logs = st.checkbox("显示入库日志", value=True)
    st.markdown("**默认导入目录**")
    st.code(str(INBOX_WEB))

uploaded_files = st.file_uploader(
    "或直接上传导出文件",
    accept_multiple_files=True,
    type=["html", "htm", "pdf", "docx", "txt", "md", "json", "enex"],
)

if st.button("开始导入", type="primary", use_container_width=True):
    raw_inputs = [line.strip() for line in url_input.splitlines() if line.strip()]
    if not raw_inputs and not uploaded_files:
        st.warning("请至少输入一个链接、本地文件路径，或上传一个导出文件。")
    else:
        results: list[dict[str, str]] = []
        with st.spinner("正在抓取并写入本地知识库..."):
            for raw in raw_inputs:
                try:
                    if re.match(r"^https?://", raw, flags=re.IGNORECASE):
                        saved = fetch_and_store(raw)
                    else:
                        saved = store_local_file(Path(raw))
                    results.append({"input": raw, "status": "saved", "detail": str(saved)})
                except Exception as exc:
                    results.append({"input": raw, "status": "error", "detail": str(exc)})
            for uploaded_file in uploaded_files or []:
                try:
                    saved = store_uploaded_file(uploaded_file)
                    results.append({"input": uploaded_file.name, "status": "saved", "detail": str(saved)})
                except Exception as exc:
                    results.append({"input": uploaded_file.name, "status": "error", "detail": str(exc)})
            ingest_stdout = ""
            ingest_stderr = ""
            ingest_code = None
            if auto_ingest and any(item["status"] == "saved" for item in results):
                ingest_code, ingest_stdout, ingest_stderr = run_ingest()

        for item in results:
            if item["status"] == "saved":
                st.success(f"已保存: {item['input']} -> {item['detail']}")
            else:
                st.error(f"导入失败: {item['input']} -> {item['detail']}")

        if auto_ingest and ingest_code is not None:
            if ingest_code == 0:
                st.success("知识库入库完成。")
            else:
                st.error(f"知识库入库失败，退出码: {ingest_code}")
            if show_logs:
                if ingest_stdout.strip():
                    st.text_area("入库输出", ingest_stdout, height=180)
                if ingest_stderr.strip():
                    st.text_area("入库错误", ingest_stderr, height=120)

st.subheader("最近入库记录")
recent = read_recent_imports()
if recent:
    rows = []
    for item in recent:
        rows.append(
            {
                "canonical_id": item.get("canonical_id", ""),
                "source_name": item.get("source_name", ""),
                "original_path": item.get("original_path", ""),
                "snapshot_path": item.get("snapshot_path", ""),
                "imported_at": item.get("imported_at", ""),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("暂无入库记录。")

st.subheader("使用说明")
st.markdown(
    "\n".join(
        [
            "- 支持公开可访问的正文链接，以及本地导出的 HTML、PDF、DOCX、ENEX 等文件。",
            "- 不要求你在界面里区分印象笔记、Get 笔记、微信或普通网页。",
            "- 对于动态页面或私有页面，优先使用“导出文件路径”或“直接上传导出文件”。",
            "- 导入后的原始文件进入 `Inbox/web`，随后进入统一知识库流程。",
        ]
    )
)
