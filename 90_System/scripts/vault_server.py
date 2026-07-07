import http.server, os, markdown, urllib.parse, mimetypes, sys

VAULT = r"D:\Obsidian"
PORT = 8899
mimetypes.add_type("text/html", ".html")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=VAULT, **kw)
    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        fp = os.path.join(VAULT, path.lstrip("/"))
        if path.endswith(".md") and os.path.isfile(fp):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    md = f.read()
                html = markdown.markdown(md, extensions=["fenced_code", "tables"])
                body = f"<!DOCTYPE html><html><head><meta charset=utf-8><style>body{{font-family:Segoe UI,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.8}}code{{background:#f0f0f0;padding:2px 6px;border-radius:4px}}pre{{background:#f5f5f5;padding:16px;border-radius:8px;overflow-x:auto}}table{{border-collapse:collapse}}th,td{{border:1px solid #ddd;padding:8px}}</style></head><body>{html}</body></html>"
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(body.encode("utf-8")))
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))
            except:
                self.send_error(500)
            return
        return super().do_GET()

sys.stdout.write("READY\n")
sys.stdout.flush()
http.server.HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
