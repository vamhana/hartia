#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Диагностика: что реально написано в статьях.

Показывает:
  - все уникальные формы слов «Статья*» и «Книга*», с частотой
  - все «см. ...» с контекстом
  - топ номеров X.Y, упомянутых в тексте, но не слинкованных

Запуск:
    python scripts/diagnose_links.py
"""

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARTER = ROOT / "src" / "content" / "charter_original"
# Если backup ещё не создан — читаем оригиналы
if not CHARTER.exists():
    CHARTER = ROOT / "src" / "content" / "charter"

RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def strip_frontmatter(text: str) -> str:
    m = RE_FRONTMATTER.match(text)
    return text[m.end():] if m else text


def main() -> int:
    if not CHARTER.exists():
        print(f"[ERR] нет {CHARTER}")
        return 1

    print(f"Читаем: {CHARTER}")
    files = list(CHARTER.glob("kniga-*/*.md"))
    print(f"Файлов: {len(files)}")
    print()

    # ─── 1. Все формы «Статья*» ───
    word_art = re.compile(r"\b(Стать[а-яё]+)", re.IGNORECASE)
    # ─── 2. Все формы «Книга*» ───
    word_book = re.compile(r"\b(Книг[а-яё]+)", re.IGNORECASE)
    # ─── 3. Все «см. ...» ───
    see_ctx = re.compile(r".{0,30}\bсм\..{0,40}", re.IGNORECASE)

    art_forms = Counter()
    book_forms = Counter()
    see_examples = []
    numbers_mentioned = Counter()

    # Какой номер после «Статья X.Y»
    art_num_re = re.compile(r"Стать[а-яё]+\s+(\d+(?:\.\d+)+)", re.IGNORECASE)

    for path in files:
        text = strip_frontmatter(path.read_text(encoding="utf-8"))

        for m in word_art.finditer(text):
            art_forms[m.group(1).lower()] += 1
        for m in word_book.finditer(text):
            book_forms[m.group(1).lower()] += 1

        for m in see_ctx.finditer(text):
            if len(see_examples) < 20:
                see_examples.append(m.group(0).strip())

        for m in art_num_re.finditer(text):
            numbers_mentioned[m.group(1)] += 1

    # ─── Отчёт ───
    print("── Формы слова «Статья» (по частоте) ──")
    for form, count in art_forms.most_common(20):
        print(f"  {form:<25} {count}")
    print()

    print("── Формы слова «Книга» (по частоте) ──")
    for form, count in book_forms.most_common(20):
        print(f"  {form:<25} {count}")
    print()

    print(f"── «см.» — примеры ({len(see_examples)}) ──")
    for ex in see_examples[:20]:
        print(f"  • {ex}")
    print()

    print("── Топ-20 упомянутых номеров (Статья X.Y) ──")
    for num, count in numbers_mentioned.most_common(20):
        print(f"  {num:<15} {count}")
    print()

    print("── Итог ──")
    print(f"  Уникальных форм «Статья*»: {len(art_forms)}")
    print(f"  Уникальных форм «Книга*»:  {len(book_forms)}")
    print(f"  Всего номеров X.Y в тексте: {sum(numbers_mentioned.values())}")
    print(f"  Уникальных номеров:         {len(numbers_mentioned)}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())