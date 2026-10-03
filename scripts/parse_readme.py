#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Разбивает README.md на статьи. v2 — дедупликация + регистр ЧАСТЬ.

Запуск:
    python scripts/parse_readme.py --dry-run
    python scripts/parse_readme.py
    python scripts/parse_readme.py --force
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT_DIR = ROOT / "src" / "content" / "charter"
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

# Книга и часть — регистронезависимо, т.к. в теле «КНИГА» и «ЧАСТЬ» капсом
RE_BOOK = re.compile(r"^\s*КНИГА\s+([IVX]+)\.\s*(.+)$", re.IGNORECASE)
RE_PART = re.compile(r"^\s*ЧАСТЬ\s+(\d+)\.\s*(.+)$", re.IGNORECASE)
RE_ARTICLE = re.compile(r"^\s*Статья\s+([\d.]+)\.\s+(.+)$")

# «(из Хартии, Ст.57)» в конце заголовка
RE_SOURCE = re.compile(r"\s*\(из\s+.+?\)\s*$")

ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
    "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
}


def parse_articles(lines: list[str]) -> list[dict]:
    """Парсит всё от начала файла. TOC и тело попадут сюда вместе."""
    articles = []
    current = None
    current_book = None
    current_book_title = ""
    current_part = None
    current_part_title = ""

    for line in lines:
        stripped = line.rstrip()

        m_book = RE_BOOK.match(stripped)
        if m_book:
            if current is not None:
                articles.append(current)
                current = None
            roman = m_book.group(1).upper()
            current_book = ROMAN.get(roman, 0)
            current_book_title = m_book.group(2).strip()
            current_part = None
            current_part_title = ""
            continue

        m_part = RE_PART.match(stripped)
        if m_part:
            if current is not None:
                articles.append(current)
                current = None
            current_part = int(m_part.group(1))
            current_part_title = m_part.group(2).strip()
            continue

        m_art = RE_ARTICLE.match(stripped)
        if m_art:
            if current is not None:
                articles.append(current)

            number = m_art.group(1)
            raw_title = m_art.group(2).strip()

            source = ""
            m_src = RE_SOURCE.search(raw_title)
            if m_src:
                source = m_src.group(0).strip("() ")
                raw_title = RE_SOURCE.sub("", raw_title).strip()

            current = {
                "number": number,
                "title": raw_title,
                "source": source,
                "book": current_book,
                "book_title": current_book_title,
                "part": current_part,
                "part_title": current_part_title,
                "body": [],
            }
            continue

        if current is not None:
            current["body"].append(line)

    if current is not None:
        articles.append(current)

    return articles


def dedup_articles(articles: list[dict]) -> list[dict]:
    """По (книга, номер) — оставить версию с самым длинным телом."""
    best: dict[tuple, dict] = {}
    for a in articles:
        if not a.get("book") or not a.get("part"):
            continue
        body_len = len("\n".join(a["body"]).strip())
        a["_body_len"] = body_len
        key = (a["book"], a["number"])
        if key not in best or body_len > best[key]["_body_len"]:
            best[key] = a
    # Отсеять TOC-пустышки
    result = [a for a in best.values() if a["_body_len"] >= 30]
    return result


def sort_and_number(articles: list[dict]) -> dict[int, list[dict]]:
    """Сгруппировать по книгам, отсортировать, присвоить order."""
    by_book: dict[int, list[dict]] = {}
    for a in articles:
        by_book.setdefault(a["book"], []).append(a)

    for book_num, arts in by_book.items():
        def sort_key(a):
            num_parts = tuple(
                int(x) for x in a["number"].split(".") if x.isdigit()
            )
            return (a["part"] or 0, num_parts)

        arts.sort(key=sort_key)
        for i, a in enumerate(arts, 1):
            a["order"] = i

    return by_book


def slug_from_number(number: str) -> str:
    return number.replace(".", "-")


def make_filename(article: dict) -> str:
    return f"{slug_from_number(article['number'])}.md"


def make_frontmatter(article: dict) -> str:
    def esc(s):
        return s.replace('"', '\\"')

    lines = [
        "---",
        f'title: "{esc(article["title"])}"',
        f'number: "{article["number"]}"',
        f"book: {article['book']}",
        f'bookTitle: "{esc(article["book_title"])}"',
        f"part: {article['part'] or 0}",
        f'partTitle: "{esc(article["part_title"])}"',
        f"order: {article['order']}",
    ]
    if article.get("source"):
        lines.append(f'source: "{esc(article["source"])}"')
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def clean_body(body_lines: list[str]) -> str:
    text = "\n".join(body_lines).strip()
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def main() -> int:
    if not README.exists():
        print(f"[ERR] нет {README}")
        return 1

    lines = README.read_text(encoding="utf-8").splitlines()
    print(f"Файл: {len(lines)} строк")
    print()

    all_articles = parse_articles(lines)
    print(f"Найдено записей (до дедупликации): {len(all_articles)}")

    deduped = dedup_articles(all_articles)
    print(f"Осталось после дедупликации:      {len(deduped)}")
    print()

    by_book = sort_and_number(deduped)

    print("── Распределение ──")
    for book_num in sorted(by_book.keys()):
        arts = by_book[book_num]
        parts = sorted(set(a["part"] for a in arts if a["part"]))
        print(f"  Книга {book_num}: {len(arts)} статей, части {parts}")
    print()

    written = skipped = 0
    for book_num, arts in by_book.items():
        for art in arts:
            rel = f"kniga-{book_num}/{make_filename(art)}"
            full = OUT_DIR / rel

            fm = make_frontmatter(art)
            body = clean_body(art["body"])
            content = fm + body + "\n"

            if full.exists() and not FORCE:
                print(f"[skip]  {rel}")
                skipped += 1
                continue

            if DRY_RUN:
                size_kb = len(content) / 1024
                title_short = art["title"][:50]
                print(f"[dry]   {rel} ({size_kb:.1f} КБ) — {title_short}")
                continue

            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(content, encoding="utf-8")
            written += 1

    print()
    if DRY_RUN:
        print(f"Режим --dry-run. Будет записано: {len(deduped)} файлов.")
    else:
        print(f"Записано: {written}, пропущено: {skipped}.")
    print()
    print("Дальше:")
    print("  Проверь src/content/charter/kniga-1/1-1.md")
    print("  Если ок — пишем page-рендер.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())