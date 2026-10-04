from pathlib import Path
import re

root = Path(__file__).resolve().parent
SITE = "https://hermanasmercedariasarroyito.vercel.app"
skip_dirs = {"PrismaWeb"}

for path in root.rglob("*"):
    if path.name == "_seo_bulk.py":
        continue
    if path.suffix.lower() not in {".html", ".xml", ".txt", ".js", ".css", ".json"}:
        continue
    rel = path.relative_to(root)
    if rel.parts and rel.parts[0] in skip_dirs:
        continue
    text = path.read_text(encoding="utf-8")
    orig = text
    text = text.replace("https://tudominio-real.com", SITE)
    if path.suffix.lower() == ".html":
        text = text.replace('href="Noticias.html"', 'href="Proyectos.html"')
        text = text.replace("href='Noticias.html'", "href='Proyectos.html'")

        def add_fd(m):
            block = m.group(0)
            if "font-display" in block:
                return block
            return block.replace(
                "format('truetype');",
                "format('truetype');\n            font-display: swap;",
            )

        text = re.sub(r"@font-face\s*\{[^}]+\}", add_fd, text)
    if text != orig:
        path.write_text(text, encoding="utf-8", newline="\n")
        print("updated", rel)
print("bulk done")
