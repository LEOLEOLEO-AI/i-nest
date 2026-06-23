import http.server, os, urllib.parse, markdown

BASE = r"D:\Obsidian\home\work\.openclaw\workspace"
PORT = 8901

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Microsoft YaHei',sans-serif;max-width:900px;margin:0 auto;padding:40px 24px;background:#fffef9;color:#1a1a2e;line-height:1.8}
h1{font-size:1.8em;margin:.5em 0 .3em;border-bottom:2px solid #1e3799;padding-bottom:.3em}
h2{font-size:1.4em;margin:1em 0 .4em;color:#1e3799;border-left:4px solid #1e3799;padding-left:10px}
table{border-collapse:collapse;width:100%;margin:.8em 0;font-size:.92em}
th{background:#1e3799;color:#fff;padding:6px 10px;text-align:left}
td{border:1px solid #dcdde1;padding:5px 10px}
tr:nth-child(even){background:#f5f6fa}
pre{background:#2d3436;color:#dfe6e9;padding:14px;border-radius:6px;overflow-x:auto}
code{background:#eef0f8;padding:1px 5px;border-radius:3px}
blockquote{border-left:4px solid #c0392b;padding:8px 16px;margin:.8em 0;background:#fef5f5}
a{color:#1e3799}
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE, **kwargs)
    def do_GET(self):
        p = os.path.join(BASE, urllib.parse.unquote(self.path.split("?")[0]).lstrip("/"))
        if os.path.isdir(p):
            p = os.path.join(p, "index.md")
        if not os.path.exists(p):
            p2 = p + ".md"
            if os.path.exists(p2): p = p2
        if not os.path.exists(p):
            self.send_error(404); return
        if p.endswith(".md"):
            md = open(p, encoding="utf-8").read()
            html = markdown.markdown(md, extensions=["tables","fenced_code"])
            html = f"<!DOCTYPE html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{html}</body></html>"
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            super().do_GET()

httpd = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
print(f"OK: http://127.0.0.1:{PORT}/")
httpd.serve_forever()
