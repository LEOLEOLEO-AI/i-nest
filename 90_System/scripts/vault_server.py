import http.server, os, urllib.parse, mimetypes, sys, traceback, time

VAULT = r"D:\Obsidian"
PORT = 8899
mimetypes.add_type("text/html", ".html")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=VAULT, **kw)

    def do_GET(self):
        try:
            path = urllib.parse.unquote(self.path.split("?")[0])
            fp = os.path.join(VAULT, path.lstrip("/"))
            if path.endswith(".md") and os.path.isfile(fp) and os.path.getsize(fp) < 5_000_000:
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        md = f.read()
                    import markdown
                    html = markdown.markdown(md, extensions=["fenced_code", "tables", "extra", "meta", "codehilite", "nl2br"])
                    body = (
                        '<!DOCTYPE html><html><head><meta charset=utf-8>'
                        '<style>body{font-family:Segoe UI,sans-serif;max-width:900px;margin:40px auto;'
                        'padding:0 20px;line-height:1.8}code{background:#f0f0f0;padding:2px 6px;'
                        'border-radius:4px}pre{background:#f5f5f5;padding:16px;border-radius:8px;'
                        'overflow-x:auto}table{border-collapse:collapse}th,td{border:1px solid #ddd;'
                        'padding:8px}</style>' + '<script>window.MathJax={tex:{inlineMath:[["$","$"],["\\(","\\)"]],displayMath:[["$$","$$"],["\\[","\\]"]]}};</script>' + '<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>' + '</head><body>' + html + '</body></html>'
                    )
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Cache-Control", "no-cache")
                    self.send_header("Content-Length", str(len(body.encode("utf-8"))))
                    self.end_headers()
                    self.wfile.write(body.encode("utf-8"))
                    return
                except Exception:
                    pass
            return super().do_GET()
        except ConnectionError:
            pass
        except Exception:
            try:
                self.send_error(500)
            except:
                pass

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    sys.stdout.write("READY\n")
    sys.stdout.flush()
    while True:
        try:
            srv = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
            srv.serve_forever()
        except OSError as e:
            if e.errno == 10048:
                time.sleep(3)
                continue
            raise
        except Exception:
            traceback.print_exc()
            time.sleep(3)
