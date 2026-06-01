#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from docx import Document

REPO_ROOT = Path(__file__).parent.parent
INCOMING = REPO_ROOT / "incoming" / "topics"
CONTENT = REPO_ROOT / "content" / "topics"

SLUG_MAP = {
    "зачинатель": "zachinatel",
    "словесность": "slovesnost",
    "завет": "zavet",
    "обязательства": "zavet",
    "время": "vremya",
    "знаки": "znaki",
    "власть": "vlast",
    "речь": "rech",
    "незримое": "nezrimoe",
    "человек": "chelovek",
    "служение": "sluzhenie",
    "семья": "semya",
    "ритуалы": "ritualy",
    "общество": "obshchestvo",
    "экономика": "ekonomika",
    "ограничения": "ogranicheniya",
    "геополитика": "geopolitika",
    "вестники": "vestniki",
    "смерть": "smert",
}

def to_slug(name):
    key = name.lower().strip()
    for ru, lat in SLUG_MAP.items():
        if key.startswith(ru):
            return lat
    return re.sub(r'[^a-z0-9]+', '-', key)

def is_heading(para):
    return (
        any(run.bold for run in para.runs if run.text.strip())
        and para.paragraph_format.left_indent is None
        and para.paragraph_format.space_before is not None
        and para.paragraph_format.space_before > 200000
    )

def is_ayat(para):
    return (
        any(run.bold for run in para.runs if run.text.strip())
        and para.paragraph_format.left_indent is not None
        and para.paragraph_format.left_indent > 400000
    )

def to_html(para):
    t = para.text.strip()
    if not t:
        return None
    if is_ayat(para):
        return f'<p class="ayat"><strong>{t}</strong></p>'
    if is_heading(para):
        return f'<h2>{t}</h2>'
    return f'<p>{t}</p>'

CSS = """<style>
.article-body{font-family:"Times New Roman",serif;font-size:1.1rem;line-height:1.9;color:#343a40}
.article-body h2{font-family:"Playfair Display",serif;font-size:1.6rem;color:#1a6b6b;margin-top:2.5rem;margin-bottom:0.8rem}
.article-body p{margin-bottom:0.8rem;text-indent:2em}
.article-body p.ayat{font-weight:bold;margin:1.2rem 0 1.2rem 3rem;text-indent:0}
</style>"""

def convert(docx_path, section):
    doc = Document(str(docx_path))
    paras = [p for p in doc.paragraphs if p.text.strip()]
    if not paras:
        print(f"SKIP (empty): {docx_path}")
        return
    title = paras[0].text.strip()
    slug = to_slug(title)
    parts = [to_html(p) for p in paras[1:]]
    parts = [h for h in parts if h]
    body = "\n".join(parts)
    final = f'---\ntitle: "{title}"\n---\n{CSS}\n<div class="article-body">\n{body}\n</div>'
    out_dir = CONTENT / section
    out_dir.mkdir(parents=True, exist_ok=True)
    out_md = out_dir / f"{slug}.md"
    out_md.write_text(final, encoding="utf-8")
    print(f"OK: {out_md} ({len(parts)} elements)")

def main():
    if len(sys.argv) == 3:
        convert(Path(sys.argv[1]), sys.argv[2])
        return
    for section_dir in sorted(INCOMING.iterdir()):
        if not section_dir.is_dir():
            continue
        section = section_dir.name
        for docx in sorted(section_dir.glob("*.docx")):
            convert(docx, section)

if __name__ == "__main__":
    main()
