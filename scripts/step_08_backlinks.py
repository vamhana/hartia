#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 8: Связанные статьи (backlinks + автолинковка). v4.

Использует маркеры {{LINK:b:num}} вместо прямой подстановки ссылок.
Это защищает от каскадных срабатываний регулярок.

Запуск:
    python scripts/step_08_backlinks.py --dry-run
    python scripts/step_08_backlinks.py
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARTER = ROOT / "src" / "content" / "charter"
BACKUP = ROOT / "src" / "content" / "charter_original"
ASTRO_CONFIG = ROOT / "astro.config.mjs"
GITIGNORE = ROOT / ".gitignore"
DRY_RUN = "--dry-run" in sys.argv

RE_BASE = re.compile(r"base:\s*['\"]([^'\"]+)['\"]")
RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# ─── Словарные формы (буква ё и е обе, регистр — ignorecase) ───
W_ART = r"(?:Стать[а-яё]+)"
W_BOOK = r"(?:Книг[а-яё]+)"
W_PART = r"(?:Част[а-яё]+)"
R = r"(I{1,3}|IV|V|VI{1,3}|IX|X)"
N = r"(\d+(?:\.\d+)+)"

# 1. Книга R, [Часть N,] Статья X.Y  — самое длинное
RE_BOOK_PART_ART = re.compile(
    rf"(?<!\[)\b{W_BOOK}\s+{R}[\s,;.—-]+(?:{W_PART}\s+\d+[\s,;.—-]+)?{W_ART}\s+{N}\b",
    re.IGNORECASE,
)

# 2. Книга R, Часть N (без Статьи)
RE_BOOK_PART = re.compile(
    rf"(?<!\[)\b{W_BOOK}\s+{R}[\s,;.—-]+{W_PART}\s+(\d+)\b",
    re.IGNORECASE,
)

# 3. Книга R
RE_BOOK = re.compile(
    rf"(?<!\[)\b{W_BOOK}\s+{R}\b",
    re.IGNORECASE,
)

# 4. [Часть N,] Статья X.Y
RE_PART_ART = re.compile(
    rf"(?<!\[)\b(?:{W_PART}\s+\d+[\s,;.—-]+)?{W_ART}\s+{N}\b",
    re.IGNORECASE,
)

# Финальный маркер
RE_MARKER = re.compile(r"\{\{LINK:(\d+):([\d.]+)\}\}")

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
         "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}
ROMAN_NAME = {v: k for k, v in ROMAN.items()}

OUT_HEADER = "## Ссылается на"
BACK_HEADER = "## Упоминается в"


def get_base() -> str:
    if not ASTRO_CONFIG.exists():
        return ""
    m = RE_BASE.search(ASTRO_CONFIG.read_text(encoding="utf-8"))
    return (m.group(1) if m else "").rstrip("/")


def parse_frontmatter(text: str):
    m = RE_FRONTMATTER.match(text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, text[m.end():]


def short_number(number: str) -> str:
    parts = number.split(".")
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else number


def slug(number: str) -> str:
    return short_number(number).replace(".", "-")


def url_for(book: int, number: str, base: str) -> str:
    return f"{base}/charter/kniga-{book}/{slug(number)}"


def load_articles():
    a = {}
    for path in sorted(CHARTER.glob("kniga-*/*.md")):
        fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        try:
            book = int(fm.get("book", 0))
            num = fm.get("number", "")
        except (ValueError, TypeError):
            continue
        if book and num:
            a[(book, short_number(num))] = path
    return a


def ensure_backup():
    if not BACKUP.exists():
        shutil.copytree(CHARTER, BACKUP)
        print("[backup] charter/ → charter_original/")
    else:
        for f in CHARTER.glob("kniga-*/*.md"):
            f.unlink()
        for f in BACKUP.glob("kniga-*/*.md"):
            target = CHARTER / f.relative_to(BACKUP)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
        print("[restore] charter/ восстановлен из charter_original/")


def ensure_gitignore():
    if DRY_RUN or not GITIGNORE.exists():
        return
    c = GITIGNORE.read_text(encoding="utf-8")
    if "charter_original" in c:
        return
    c = c.rstrip() + "\n\n# Charter backup\nsrc/content/charter_original/\n"
    GITIGNORE.write_text(c, encoding="utf-8")
    print("[gitignore] добавлен src/content/charter_original/")


def link_body(body: str, current_book: int, all_articles, base: str):
    targets: set[tuple[int, str]] = set()
    stats = {"book_part_art": 0, "book_part": 0, "book": 0, "part_art": 0}

    def resolve(book: int, number: str):
        short = short_number(number)
        if (book, short) in all_articles:
            return (book, short)
        if (current_book, short) in all_articles:
            return (current_book, short)
        for (b, n) in all_articles:
            if n == short:
                return (b, n)
        return None

    def repl_bpa(m: re.Match) -> str:
        roman, number = m.group(1), m.group(2)
        book = ROMAN.get(roman.upper(), 0)
        if not book:
            return m.group(0)
        res = resolve(book, number)
        if not res:
            return m.group(0)
        b, n = res
        targets.add(res)
        stats["book_part_art"] += 1
        return f"Книга {roman}, Статья {number} {{{{LINK:{b}:{n}}}}}"

    def repl_bp(m: re.Match) -> str:
        roman = m.group(1)
        book = ROMAN.get(roman.upper(), 0)
        if not book:
            return m.group(0)
        stats["book_part"] += 1
        return m.group(0)

    def repl_book(m: re.Match) -> str:
        roman = m.group(1)
        book = ROMAN.get(roman.upper(), 0)
        if not book:
            return m.group(0)
        stats["book"] += 1
        return f"[Книга {roman}]({base}/charter/kniga-{book})"

    def repl_pa(m: re.Match) -> str:
        number = m.group(1)
        res = resolve(current_book, number)
        if not res:
            return m.group(0)
        b, n = res
        if b == current_book and n == short_number(number) and number == short_number(number):
            return m.group(0)
        targets.add(res)
        stats["part_art"] += 1
        return f"Статья {number} {{{{LINK:{b}:{n}}}}}"

    # Порядок: длинные → короткие. Каждая замена оставляет маркер,
    # который не содержит слов «Книга»/«Статья»/«Часть»,
    # поэтому следующие regex его не тронут.
    body = RE_BOOK_PART_ART.sub(repl_bpa, body)
    body = RE_BOOK_PART.sub(repl_bp, body)      # заглушка, чтобы потом не поймать
    body = RE_BOOK.sub(repl_book, body)
    body = RE_PART_ART.sub(repl_pa, body)

    return body, targets, stats


def finalize_markers(text: str, base: str) -> str:
    """{{LINK:b:n}} → [Статья N](url)."""
    def r(m):
        b, n = int(m.group(1)), m.group(2)
        return f"[Статья {n}]({url_for(b, n, base)})"
    return RE_MARKER.sub(r, text)


def make_section(header: str, items, all_articles, base: str) -> str:
    lines = [header, ""]
    for (b, n) in sorted(items, key=lambda x: (x[0], x[1])):
        p = all_articles.get((b, n))
        if not p:
            continue
        fm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
        title = fm.get("title", "")
        roman = ROMAN_NAME.get(b, str(b))
        lines.append(f"- Книга {roman}, [Статья {n}. {title}]({url_for(b, n, base)})")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not CHARTER.exists():
        print(f"[ERR] нет {CHARTER}")
        return 1

    base = get_base()
    print(f"Проект: {ROOT}")
    print(f"base:   {base or '(пусто)'}")
    if DRY_RUN: print("Режим:  --dry-run")
    print()

    ensure_gitignore()
    if not DRY_RUN:
        ensure_backup()
    print()

    all_articles = load_articles()
    print(f"Найдено статей: {len(all_articles)}")

    processed = {}
    incoming = {}
    outgoing_map = {}
    total_stats = {"book_part_art": 0, "book_part": 0, "book": 0, "part_art": 0}

    for (book, num), path in all_articles.items():
        text = path.read_text(encoding="utf-8")
        fm_match = RE_FRONTMATTER.match(text)
        if not fm_match:
            continue
        fm_text = fm_match.group(0)
        body = text[len(fm_text):]

        new_body, targets, stats = link_body(body, book, all_articles, base)
        new_body = finalize_markers(new_body, base)

        processed[path] = (fm_text, new_body, (book, num))
        outgoing_map[(book, num)] = targets
        for k in stats:
            total_stats[k] += stats[k]
        for t in targets:
            incoming.setdefault(t, set()).add((book, num))

    print()
    print("── Статистика подстановок ──")
    print(f"  Книга + [Часть] + Статья: {total_stats['book_part_art']}")
    print(f"  Книга + Часть (без статьи): {total_stats['book_part']}  (не линкуется, но находим)")
    print(f"  Книга отдельно:             {total_stats['book']}")
    print(f"  [Часть] + Статья:           {total_stats['part_art']}")
    print(f"  ВСЕГО ссылок на статьи:     {total_stats['book_part_art'] + total_stats['part_art']}")
    print(f"  ВСЕГО ссылок на книги:      {total_stats['book']}")
    print()

    total_out = sum(len(v) for v in outgoing_map.values())
    orphans_in = sum(1 for k in all_articles if k not in incoming)
    print(f"Уникальных целей линковки: {total_out}")
    print(f"Статей без входящих:       {orphans_in}")
    print()

    top_in = sorted(incoming.items(), key=lambda x: -len(x[1]))[:10]
    print("── Топ-10 самых цитируемых ──")
    for (book, num), sources in top_in:
        p = all_articles.get((book, num))
        title = ""
        if p:
            fm, _ = parse_frontmatter(p.read_text(encoding="utf-8"))
            title = fm.get("title", "")[:45]
        roman = ROMAN_NAME.get(book, str(book))
        print(f"  Книга {roman}, {num}. {title} — {len(sources)} входящих")
    print()

    written = 0
    for path, (fm_text, new_body, (book, num)) in processed.items():
        bl = incoming.get((book, num), set())
        out = outgoing_map.get((book, num), set())
        out = {t for t in out if t != (book, num)}

        extra = []
        if out:
            extra.append(make_section(OUT_HEADER, out, all_articles, base))
        if bl:
            extra.append(make_section(BACK_HEADER, bl, all_articles, base))

        if extra:
            new_body = new_body.rstrip() + "\n\n" + "\n".join(extra)

        final = fm_text + new_body
        if not final.endswith("\n"):
            final += "\n"

        if DRY_RUN:
            continue
        path.write_text(final, encoding="utf-8")
        written += 1

    print()
    if DRY_RUN:
        print("Режим --dry-run. Ничего не записано.")
    else:
        print(f"Записано: {written} статей")
    print()
    print("Дальше:")
    print("  npm run dev")
    print("  Проверь http://localhost:4321/hartia/charter/kniga-1/1-10")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())