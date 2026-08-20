from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


DEFAULT_INBOX = Path(r"D:\\Obsidian\\Agent\01-Theory-Research\Inbox\enote")
DEFAULT_INGEST_SCRIPT = Path(r"D:\\Obsidian\\Agent\scripts\knowledge_base_ingest.py")
DEFAULT_CONFIG = Path(r"D:\\Obsidian\\Agent\01-Theory-Research\knowledge_base_config.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export an Evernote shared note page to the local knowledge base inbox.")
    parser.add_argument("url", help="Evernote shared note URL")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_INBOX),
        help="Directory where the downloaded HTML file will be saved.",
    )
    parser.add_argument(
        "--import-now",
        action="store_true",
        help="Run the local knowledge base ingest script after saving the HTML file.",
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Path to the knowledge base config JSON used by the ingest script.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP timeout in seconds.",
    )
    return parser.parse_args()


def safe_filename(name: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", name).strip("_")
    return value or "evernote_note"


def infer_title(html_text: str, fallback: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    if not title:
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()
    return title or fallback


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise SystemExit("URL must start with http:// or https://")
    if not parsed.netloc:
        raise SystemExit("URL is missing a hostname")


def fetch_html(url: str, timeout: int) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.encoding or response.apparent_encoding or "utf-8"
    return response.text


def save_html(url: str, html_text: str, output_dir: Path) -> Path:
    today_dir = output_dir / datetime.now().strftime("%Y%m%d")
    today_dir.mkdir(parents=True, exist_ok=True)
    title = infer_title(html_text, "evernote_note")
    file_path = today_dir / f"{safe_filename(title)}.html"
    counter = 2
    while file_path.exists():
        file_path = today_dir / f"{safe_filename(title)}_{counter}.html"
        counter += 1
    file_path.write_text(html_text, encoding="utf-8")
    return file_path


def run_ingest(config_path: Path) -> int:
    command = [
        "python",
        str(DEFAULT_INGEST_SCRIPT),
        "--config",
        str(config_path),
    ]
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    args = parse_args()
    validate_url(args.url)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    html_text = fetch_html(args.url, args.timeout)
    saved_path = save_html(args.url, html_text, output_dir)
    print(f"Saved shared note HTML to: {saved_path}")

    if args.import_now:
        code = run_ingest(Path(args.config))
        if code != 0:
            print(f"Ingest script failed with exit code: {code}")
            return code
        print("Knowledge base ingest completed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
