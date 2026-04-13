#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INCOMING = REPO_ROOT / "incoming" / "topics"
CONTENT = REPO_ROOT / "content" / "topics"

SLUG_MAP = {
    "зачинатель": "zachinatel",
    "словесность": "slovesnost",
    "завет": "zavet",
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

def get_title_from_docx(docx_path):
    try:
        from docx import Document
        doc = Document(str(docx_path))
        for para in doc.paragraphs:
            if para.text.strip():
                return para.text.strip()
    except Exception:
        pass
    return docx_path.stem

def to_slug(name):
    key = name.lower().strip()
    for ru, lat in SLUG_MAP.items():
        if key.startswith(ru):
            return lat
    return re.sub(r'[^a-z0-9]+', '-', key)

def process_ayats(md_text):
    lines = md_text.splitlines()
    result = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\*\*.+\(\d+:\d+\)\*\*$', stripped):
            inner = stripped[2:-2]
            result.append(f'{{{{< ayah >}}}}{inner}{{{{< /ayah >}}}}')
        else:
            result.append(line)
    return "\n".join(result)

def convert(docx_path, section):
    title = get_title_from_docx(docx_path)
    slug = to_slug(title)

    out_dir = CONTENT / section
    out_dir.mkdir(parents=True, exist_ok=True)
    out_md = out_dir / f"{slug}.md"

    result = subprocess.run(
        ["pandoc", str(docx_path), "-t", "markdown", "--wrap=none"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Ошибка pandoc: {result.stderr}")
        return False

    md = result.stdout
    lines = md.splitlines()
    body_lines = [l for l in lines if not l.startswith("# ")]
    body = process_ayats("\n".join(body_lines))

    pdf_name = f"/{slug}.pdf"
    final = f'---\ntitle: "{title}"\npdf: "{pdf_name}"\n---\n\n{body}'
    out_md.write_text(final, encoding="utf-8")
    print(f"OK: {out_md} (title={title}, slug={slug})")
    return True

def main():
    if len(sys.argv) == 3:
        convert(Path(sys.argv[1]), sys.argv[2])
        return
    for section_dir in INCOMING.iterdir():
        if not section_dir.is_dir():
            continue
        section = section_dir.name
        for docx in section_dir.glob("*.docx"):
            convert(docx, section)

if __name__ == "__main__":
    main()
