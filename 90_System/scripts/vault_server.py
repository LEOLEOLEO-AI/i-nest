import http.server, os, urllib.parse, mimetypes, sys, re
from markdown_it import MarkdownIt
from mdit_py_plugins.texmath import texmath_plugin
from mdit_py_plugins.gfm import gfm_plugin, front_matter_plugin

VAULT = r"D:\Obsidian"
PORT = 8899
mimetypes.add_type("text/html", ".html")

md = MarkdownIt().use(front_matter_plugin).use(gfm_plugin).use(texmath_plugin)

MATHJAX = """<script>
window.MathJax={tex:{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']]},svg:{fontCache:'global'}};
</script>
<script src="https://cdn.bootcdn.net/ajax/libs/mathjax/3.2.2/es5/tex-svg.min.js"></script>"""

CSS = """body{font-family:'Segoe UI',sans-serif;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.8;color:#1a1a1a}
h1{font-size:1.8em;border-bottom:3px solid #002FA7;padding-bottom:8px;margin-top:0}
h2{font-size:1.4em;border-bottom:2px solid #e0e0e0;padding-bottom:6px;margin-top:32px}
h3{font-size:1.15em;margin-top:24px}
code{background:#f0f0f0;padding:2px 6px;border-radius:4px;font-size:0.9em}
pre{background:#f5f5f5;padding:16px;border-radius:8px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{border-left:4px solid #002FA7;padding:8px 16px;margin:16px 0;background:#f8f9ff}
table{border-collapse:collapse;width:100%;margin:16px 0}
th,td{border:1px solid #ddd;padding:8px 12px;text-align:left}
th{background:#002FA7;color:#fff;font-weight:600}
tr:nth-child(even){background:#f9f9f9}
a{color:#002FA7;text-decoration:none}
a:hover{text-decoration:underline}
hr{border:none;border-top:1px solid #e0e0e0;margin:32px 0}
p{margin:12px 0}
ul,ol{margin:8px 0;padding-left:24px}
.math.display{display:block;text-align:center;margin:16px 0}"""

def convert_math_tags(html):
    """Convert texmath <eq>/<eqn> tags to standard MathJax $/$$ delimiters."""
    # Display math: <section><eqn>...</eqn></section> -> $$...$$
    html = re.sub(r'<section>\s*<eqn>(.*?)</eqn>\s*</section>', r'<p class="math display">$$\1$$</p>', html, flags=re.DOTALL)
    # Inline math: <eq>...</eq> -> $...$
    html = re.sub(r'<eq>(.*?)</eq>', r'$\1$', html)
    return html

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=VAULT, **kw)
    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])
        fp = os.path.join(VAULT, path.lstrip("/"))
        if path.endswith(".md") and os.path.isfile(fp):
            try:
                with open(fp, "r", encoding="utf-8-sig") as f:
                    html = md.render(f.read())
                html = convert_math_tags(html)
                body = "<!DOCTYPE html><html><head><meta charset=utf-8>" + MATHJAX + "<style>" + CSS + "</style></head><body>" + html + "</body></html>"
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                data = body.encode("utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_error(500, str(e))
            return
        return super().do_GET()

sys.stdout.write("READY\n")
sys.stdout.flush()
http.server.HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
