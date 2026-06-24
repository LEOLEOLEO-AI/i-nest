import http.server, os, markdown, urllib.parse, mimetypes

VAULT = r"D:\Obsidian\home\work\.openclaw\workspace"
PORT = 8900
mimetypes.add_type("text/html", ".html")
mimetypes.add_type("text/plain", ".md")

class VaultHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=VAULT, **kwargs)

    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        fspath = os.path.join(VAULT, path.lstrip("/"))
        if path.endswith(".md") and os.path.isfile(fspath):
            try:
                with open(fspath, "r", encoding="utf-8") as f:
                    md_content = f.read()
                html = markdown.markdown(md_content, extensions=["fenced_code", "tables"])
                full = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{os.path.basename(fspath)}</title>
<style>body{{font-family:-apple-system,Segoe UI,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.8;color:#333;background:#fff}}h1,h2,h3{{color:#1a1a2e}}code{{background:#f0f0f0;padding:2px 6px;border-radius:4px}}pre{{background:#f5f5f5;padding:16px;border-radius:8px;overflow-x:auto}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #ddd;padding:8px 12px;text-align:left}}th{{background:#f0f0f0}}a{{color:#2563eb}}</style></head><body>{html}</body></html>"""
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(full.encode("utf-8")))
                self.end_headers()
                self.wfile.write(full.encode("utf-8"))
            except Exception as e:
                self.send_error(500, str(e))
            return
        return super().do_GET()

print(f"Vault server: http://127.0.0.1:{PORT}")
http.server.HTTPServer(("127.0.0.1", PORT), VaultHandler).serve_forever()
