#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Анализ README.md перед разбиением на статьи.

Ничего не пишет. Только читает и печатает структуру.

Запуск:
    python scripts/analyze_readme.py
"""

import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"


def main() -> int:
    if not README.exists():
        print(f"[ERR] нет файла: {README}")
        return 1

    text = README.read_text(encoding="utf-8")
    lines = text.splitlines()

    print(f"── Файл ──")
    print(f"  Путь:      {README}")
    print(f"  Размер:    {README.stat().st_size:,} байт")
    print(f"  Строк:     {len(lines):,}")
    print(f"  Символов:  {len(text):,}")
    print()

    # ── 1. Заголовки книг ──
    print("── 1. Книги ──")
    books = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^#*\s*КНИГА\s+([IVX]+)\.\s*(.+)$", line.strip())
        if m:
            books.append((i, m.group(1), m.group(2).strip()))
    for i, num, title in books:
        print(f"  Строка {i:>5}: КНИГА {num}. {title}")
    print(f"  Всего найдено: {len(books)}")
    print()

    # ── 2. Части ──
    print("── 2. Части ──")
    parts = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^#*\s*Часть\s+(\d+)\.\s*(.+)$", line.strip())
        if m:
            parts.append((i, m.group(1), m.group(2).strip()))
    for i, num, title in parts[:20]:
        print(f"  Строка {i:>5}: Часть {num}. {title[:70]}")
    if len(parts) > 20:
        print(f"  ... и ещё {len(parts) - 20}")
    print(f"  Всего найдено: {len(parts)}")
    print()

    # ── 3. Статьи ──
    print("── 3. Статьи ──")
    articles = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^#*\s*Статья\s+([\d.]+)\.\s*(.+)$", line.strip())
        if m:
            articles.append((i, m.group(1), m.group(2).strip()))

    print(f"  Всего найдено: {len(articles)}")
    print()
    print("  Первые 10:")
    for i, num, title in articles[:10]:
        print(f"    Строка {i:>5}: Статья {num}. {title[:60]}")

    print()
    print("  Последние 5:")
    for i, num, title in articles[-5:]:
        print(f"    Строка {i:>5}: Статья {num}. {title[:60]}")
    print()

    # ── 4. Проверка нумерации ──
    print("── 4. Проверка нумерации статей ──")
    numbers = [num for _, num, _ in articles]
    expected_pattern = re.compile(r"^\d+\.\d+(\.\d+)?$")
    bad_format = [n for n in numbers if not expected_pattern.match(n)]
    if bad_format:
        print(f"  ⚠ Странный формат номеров: {bad_format[:10]}")
    else:
        print("  ✓ Формат X.Y или X.Y.Z — единый")

    dupes = [n for n, c in Counter(numbers).items() if c > 1]
    if dupes:
        print(f"  ⚠ Дубликаты номеров: {dupes[:10]}")
    else:
        print("  ✓ Дубликатов нет")
    print()

    # ── 5. Оглавление vs полный текст ──
    print("── 5. Оглавление в начале ──")
    # Оглавление обычно идёт до первой "Статья 1.1"
    if articles:
        first_article_line = articles[0][0]
        head = "\n".join(lines[:first_article_line])
        print(f"  Первая статья начинается на строке: {first_article_line}")
        print(f"  Строк до неё: {first_article_line}")
        # Ищем в этой части строки вида "Статья X.Y. ..." без текста
        toc_like = re.findall(r"Статья\s+[\d.]+", head)
        print(f"  Упоминаний «Статья X.Y» до первой статьи: {len(toc_like)}")
        if toc_like:
            print("  ⚠ В начале, похоже, есть оглавление — его надо исключить")
    print()

    # ── 6. Пример статьи целиком ──
    print("── 6. Пример: статья 1.10 ──")
    for idx, (i, num, title) in enumerate(articles):
        if num == "1.10":
            start = i - 1
            end = articles[idx + 1][0] - 1 if idx + 1 < len(articles) else len(lines)
            sample = "\n".join(lines[start:min(end, start + 15)])
            print(f"  {sample[:500]}")
            break
    print()

    # ── 7. Итог ──
    print("── Итог ──")
    print(f"  Книг:     {len(books)}")
    print(f"  Частей:   {len(parts)}")
    print(f"  Статей:   {len(articles)}")
    print()
    print("Если структура выглядит верно — пишем парсер.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())