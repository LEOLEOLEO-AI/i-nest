import http.server, os, urllib.parse, mimetypes, sys, re
from markdown_it import MarkdownIt
from mdit_py_plugins.texmath import texmath_plugin

VAULT = r"D:\Obsidian"
PORT = 8899
mimetypes.add_type("text/html", ".html")

md = MarkdownIt().use(texmath_plugin)

MATHJAX = """<script>
window.MathJax={tex:{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']]},svg:{fontCache:'global'}};
</script>
<script src="https://cdn.bootcdn.net/ajax/libs/mathjax/3.2.2/es5/tex-svg.min.js"></script>"""

CSS = """body{font-family:Segoe UI,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.8}
code{background:#f0f0f0;padding:2px 6px;border-radius:4px}
pre{background:#f5f5f5;padding:16px;border-radius:8px;overflow-x:auto}
table{border-collapse:collapse}
th,td{border:1px solid #ddd;padding:8px}
th{background:#002FA7;color:#fff}"""

def clean_math_html(html):
    """Remove stray $ that texmath leaves outside <eq> tags."""
    # Remove $ right before </eq>
    html = re.sub(r'\$(</eq>)', r'\1', html)
    # Remove $ right after <eq>
    html = re.sub(r'(<eq[^>]*>)\$', r'\1', html)
    # Remove standalone $ that are adjacent to math tags
    html = re.sub(r'</eq>\$', r'</eq>', html)
    html = re.sub(r'\$<eq', r'<eq', html)
    # Remove stray $$ pairs around eq tags
    html = re.sub(r'\$\$(</?eq[^>]*>)\$\$', r'\1', html)
    return html

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=VAULT, **kw)
    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        fp = os.path.join(VAULT, path.lstrip("/"))
        if path.endswith(".md") and os.path.isfile(fp):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    html = md.render(f.read())
                html = clean_math_html(html)
                body = "<!DOCTYPE html><html><head><meta charset=utf-8>" + MATHJAX + "<style>" + CSS + "</style></head><body>" + html + "</body></html>"
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                data = body.encode("utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except:
                self.send_error(500)
            return
        return super().do_GET()

sys.stdout.write("READY\n")
sys.stdout.flush()
http.server.HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
