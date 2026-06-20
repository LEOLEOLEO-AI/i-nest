import argparse
import html
import os
import re
from datetime import datetime
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter


def strip_yaml_front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


def obsidian_to_markdown_links(text: str) -> str:
    def normalize_target(target: str) -> str:
        target = target.strip()
        if target.lower().endswith(".md"):
            target = target[:-3] + ".html"
        elif "." not in Path(target).name:
            target = target + ".html"
        return target

    text = re.sub(r"!\[\[(.+?)\]\]", lambda m: f"![]({m.group(1).strip()})", text)

    def repl_alias(m: re.Match) -> str:
        target = normalize_target(m.group(1))
        alias = m.group(2).strip()
        return f"[{alias}]({target})"

    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", repl_alias, text)

    def repl_plain(m: re.Match) -> str:
        target = m.group(1)
        target_norm = normalize_target(target)
        label = target.strip()
        return f"[{label}]({target_norm})"

    text = re.sub(r"\[\[([^\]]+)\]\]", repl_plain, text)
    return text


def infer_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def render_markdown(md_text: str) -> tuple[str, str, str]:
    md = markdown.Markdown(
        extensions=[
            "extra",
            "toc",
            "fenced_code",
            "codehilite",
        ],
        extension_configs={
            "toc": {"permalink": True},
            "codehilite": {"guess_lang": True, "noclasses": False},
        },
        output_format="html5",
    )
    body_html = md.convert(md_text)
    toc_html = md.toc
    pygments_css = HtmlFormatter().get_style_defs(".codehilite")
    return body_html, toc_html, pygments_css


def build_html(title: str, body_html: str, toc_html: str, pygments_css: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title_esc = html.escape(title)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title_esc}</title>
  <style>
    :root {{
      --bg: #0b0f14;
      --panel: #0f1720;
      --text: #e6edf3;
      --muted: #9aa4af;
      --border: #243040;
      --link: #79c0ff;
      --code-bg: #0d1117;
    }}
    html, body {{
      height: 100%;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
      line-height: 1.6;
    }}
    a {{
      color: var(--link);
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(11, 15, 20, 0.92);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border);
    }}
    .topbar-inner {{
      display: flex;
      gap: 12px;
      align-items: baseline;
      padding: 14px 18px;
      max-width: 1200px;
      margin: 0 auto;
    }}
    .title {{
      font-size: 18px;
      font-weight: 600;
      margin: 0;
    }}
    .meta {{
      color: var(--muted);
      font-size: 12px;
    }}
    .layout {{
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      gap: 18px;
      max-width: 1200px;
      margin: 0 auto;
      padding: 18px;
    }}
    .toc {{
      position: sticky;
      top: 64px;
      align-self: start;
      max-height: calc(100vh - 90px);
      overflow: auto;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 12px 14px;
    }}
    .toc > ul {{
      margin: 0;
      padding-left: 18px;
    }}
    .toc a {{
      color: var(--text);
    }}
    .content {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px 18px 26px;
      overflow: hidden;
    }}
    .content > :first-child {{
      margin-top: 0;
    }}
    h1, h2, h3, h4 {{
      line-height: 1.25;
      margin: 24px 0 12px;
    }}
    h1 {{
      font-size: 30px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border);
    }}
    h2 {{
      font-size: 22px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(36, 48, 64, 0.5);
    }}
    h3 {{
      font-size: 18px;
    }}
    p {{
      margin: 12px 0;
    }}
    blockquote {{
      margin: 12px 0;
      padding: 0 14px;
      border-left: 3px solid var(--border);
      color: var(--muted);
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.1em 0.35em;
      font-size: 0.95em;
    }}
    pre code {{
      padding: 0;
      border: 0;
      background: transparent;
    }}
    pre {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 14px;
      overflow: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      display: block;
      overflow: auto;
      border: 1px solid var(--border);
      border-radius: 10px;
    }}
    thead th {{
      position: sticky;
      top: 0;
      background: #111b26;
      z-index: 1;
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      border-right: 1px solid rgba(36, 48, 64, 0.5);
      vertical-align: top;
      min-width: 140px;
    }}
    tr:last-child td {{
      border-bottom: 0;
    }}
    th:last-child, td:last-child {{
      border-right: 0;
    }}
    ul, ol {{
      padding-left: 22px;
    }}
    hr {{
      border: 0;
      border-top: 1px solid var(--border);
      margin: 20px 0;
    }}
    {pygments_css}
    @media (max-width: 980px) {{
      .layout {{
        grid-template-columns: 1fr;
      }}
      .toc {{
        position: static;
        max-height: none;
      }}
    }}
  </style>
</head>
<body>
  <div class="topbar">
    <div class="topbar-inner">
      <div class="title">{title_esc}</div>
      <div class="meta">导出时间：{html.escape(now)}</div>
    </div>
  </div>
  <div class="layout">
    <aside class="toc">{toc_html}</aside>
    <main class="content">{body_html}</main>
  </div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Markdown file path")
    parser.add_argument("-o", "--output", help="Output HTML file path")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(str(input_path))

    output_path = Path(args.output).expanduser().resolve() if args.output else input_path.with_suffix(".html")

    text = input_path.read_text(encoding="utf-8")
    text = strip_yaml_front_matter(text)
    text = obsidian_to_markdown_links(text)

    title = infer_title(text, input_path.stem)
    body_html, toc_html, pygments_css = render_markdown(text)
    html_text = build_html(title, body_html, toc_html, pygments_css)

    output_path.write_text(html_text, encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

