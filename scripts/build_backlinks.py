#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Строит обратные ссылки «Упоминается в» для статей Хартии.

Запуск:
    python scripts/build_backlinks.py --dry-run
    python scripts/build_backlinks.py

Читает src/content/charter/**/*.md, находит в теле упоминания других
статей по паттернам «Книга X, Статья Y.Z» / «Кн. X, §Y.Z» и добавляет
в конец каждого файла блок «## Упоминается в» со ссылками на источники.
"""

import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src" / "content" / "charter"
DRY_RUN = "--dry-run" in sys.argv

# Паттерны ссылок в тексте Хартии
# «Книга VI, Статья 2.7» / «Книга 6, Статья 2.7»
RE_REF = re.compile(
    r"Книг[аеу]?\s+([IVX]+|\d+)[,\s]+(?:Статья|ст\.|§)\s*([\d.]+)",
    re.IGNORECASE,
)
# «Кн. VI, ч. 2» / «Кн. 6, §2.7» — тоже считаем
RE_REF_SHORT = re.compile(
    r"Кн\.\s*([IVX]+|\d+)[,\s]+(?:ч\.\s*\d+[,\s]+)?(?:Статья|ст\.|§)\s*([\d.]+)",
    re.IGNORECASE,
)

ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
}


def book_num(raw: str) -> int | None:
    raw = raw.upper()
    if raw in ROMAN:
        return ROMAN[raw]
    if raw.isdigit():
        return int(raw)
    return None


def slug(number: str) -> str:
    return number.replace(".", "-")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Возвращает (frontmatter-как-dict, тело)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    fm_raw = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")

    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def collect_refs(body: str) -> set[tuple[int, str]]:
    """Извлекает все ссылки (book, number) из текста."""
    refs = set()
    for regex in (RE_REF, RE_REF_SHORT):
        for m in regex.finditer(body):
            b = book_num(m.group(1))
            num = m.group(2).rstrip(".")
            if b:
                refs.add((b, num))
    return refs


def build_backlinks() -> dict[tuple[int, str], list[tuple[int, str, str]]]:
    """target (book, num) → список источников (book, num, title)."""
    articles = []  # (book, num, title, refs)
    for path in CONTENT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm.get("book") or not fm.get("number"):
            continue
        try:
            b = int(fm["book"])
        except ValueError:
            continue
        num = fm["number"]
        title = fm.get("title", "")
        refs = collect_refs(body)
        articles.append((b, num, title, refs))

    backlinks: dict[tuple[int, str], list[tuple[int, str, str]]] = {}
    for src_book, src_num, src_title, refs in articles:
        for tgt in refs:
            if tgt == (src_book, src_num):
                continue
            backlinks.setdefault(tgt, []).append((src_book, src_num, src_title))
    return backlinks


def render_block(backlinks: list[tuple[int, str, str]], base: str) -> str:
    lines = ["", "## Упоминается в", ""]
    for b, num, title in sorted(backlinks):
        href = f"{base}/charter/kniga-{b}/{slug(num)}"
        lines.append(f"- Книга {b}, [Статья {num}. {title}]({href})")
    return "\n".join(lines)


def strip_existing_block(body: str) -> str:
    """Удаляет уже существующий блок «## Упоминается в», чтобы не дублировать."""
    return re.sub(
        r"\n*## Упоминается в\n(?:.*\n)*?(?=\Z|\n##)",
        "\n",
        body,
        flags=re.MULTILINE,
    ).rstrip() + "\n"


def main() -> int:
    if not CONTENT.exists():
        print(f"[ERR] нет {CONTENT}")
        return 1

    # base URL из astro.config.mjs — грубо, но работает
    base = "/hartia"
    astro_cfg = (ROOT / "astro.config.mjs")
    if astro_cfg.exists():
        m = re.search(r'base:\s*[\'"]([^\'"]+)[\'"]', astro_cfg.read_text(encoding="utf-8"))
        if m:
            base = m.group(1).rstrip("/")

    backlinks = build_backlinks()
    print(f"Статей с обратными ссылками: {len(backlinks)}")
    print(f"Base URL: {base}")

    updated = 0
    for path in CONTENT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not fm.get("book") or not fm.get("number"):
            continue
        try:
            b = int(fm["book"])
        except ValueError:
            continue
        key = (b, fm["number"])
        srcs = backlinks.get(key, [])

        clean_body = strip_existing_block(body)
        if not srcs:
            new_text = text[: len(text) - len(body)] + clean_body
        else:
            block = render_block(srcs, base)
            new_text = text[: len(text) - len(body)] + clean_body.rstrip() + "\n" + block + "\n"

        if new_text != text:
            if DRY_RUN:
                print(f"[dry] {path.relative_to(CONTENT)} (+{len(srcs)} ссылок)")
            else:
                path.write_text(new_text, encoding="utf-8")
            updated += 1

    if DRY_RUN:
        print(f"\nБудет обновлено: {updated} файлов.")
    else:
        print(f"\nОбновлено: {updated} файлов.")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_backlinks.py")], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())