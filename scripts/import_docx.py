#!/usr/bin/env python3
import os
import sys
import subprocess
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INCOMING = REPO_ROOT / "incoming" / "topics"
CONTENT = REPO_ROOT / "content" / "topics"
MANIFEST = REPO_ROOT / "data" / "imports" / "manifest.json"

def get_title(md_text):
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Без названия"

def process_ayats(md_text):
    lines = md_text.splitlines()
    result = []
    for line in lines:
        stripped = line.strip()
        # Аят: жирная строка содержащая номер в скобках в конце типа (2:255)
        import re
        if re.match(r'^\*\*.+\(\d+:\d+\)\*\*$', stripped):
            inner = stripped[2:-2]  # убрать ** с обеих сторон
            result.append(f'{{{{< ayah >}}}}{inner}{{{{< /ayah >}}}}')
        else:
            result.append(line)
    return "\n".join(result)

def convert(docx_path, section, slug):
    out_dir = CONTENT / section
    out_dir.mkdir(parents=True, exist_ok=True)
    out_md = out_dir / f"{slug}.md"

    # Конвертируем через pandoc
    result = subprocess.run(
        ["pandoc", str(docx_path), "-t", "markdown", "--wrap=none"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Ошибка pandoc: {result.stderr}")
        return False

    md = result.stdout
    title = get_title(md)

    # Убираем первый H1 из тела
    lines = md.splitlines()
    body_lines = [l for l in lines if not l.startswith("# ")]
    body = "\n".join(body_lines)

    # Постобработка аятов
    body = process_ayats(body)

    # Frontmatter
    frontmatter = f'''---
title: "{title}"
pdf: "/{slug}.pdf"
---

'''
    final = frontmatter + body
    out_md.write_text(final, encoding="utf-8")
    print(f"OK: {out_md}")
    return True

def main():
    if len(sys.argv) == 3:
        # Прямой вызов: python3 import_docx.py file.docx section
        docx = Path(sys.argv[1])
        section = sys.argv[2]
        slug = docx.stem.lower().replace(" ", "-")
        convert(docx, section, slug)
        return

    # Авто-режим: сканируем incoming/
    for section_dir in INCOMING.iterdir():
        if not section_dir.is_dir():
            continue
        section = section_dir.name
        for docx in section_dir.glob("*.docx"):
            slug = docx.stem.lower().replace(" ", "-")
            convert(docx, section, slug)

if __name__ == "__main__":
    main()
