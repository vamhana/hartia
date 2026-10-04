#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 11: сбор упоминаний направлений в Хартии.

Читает charter_original/ (чистые статьи), для каждого из 17 направлений
ищет упоминания по ключевым стемам, складывает в JSON.

Запуск:
    python scripts\step_11_direction_mentions.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHARTER = ROOT / "src" / "content" / "charter_original"
if not CHARTER.exists():
    CHARTER = ROOT / "src" / "content" / "charter"

OUT = ROOT / "src" / "data" / "direction-mentions.json"

# ─── Стемы для поиска. Ключ — id направления, значение — список регексов ───
PATTERNS: dict[int, list[str]] = {
    1:  [r"Жизнеобеспеч"],
    2:  [
        r"\bЗдрави[еяюи]",
        r"\bЗдоров",
        r"\bМедицин",
        r"\bЛечен",
        r"\bДиагност",
        r"\bРеабилитац",
    ],
    3:  [r"Энерги[ияю] и Сред", r"Энергия и Среда"],
    4:  [r"Трансляц"],
    5:  [r"Когнитивн\w*\s+Логист"],
    6:  [r"Ноолог"],
    7:  [r"Инженери\w*\s+Обнулени", r"Обнулени"],
    8:  [r"Балансировк", r"Балансировщик"],
    9:  [r"Кибернетик"],
    10: [r"Искусств\w*\s+и\s+Резонанс", r"\bИскусств"],
    11: [r"Социальн\w*\s+Инкубац", r"\bИнкубац"],
    12: [r"Психоэколог"],
    13: [r"Верификаци", r"Верификатор"],
    14: [r"\bЗнани[еяюи]\s+и\s+Образовани", r"\bОбразовани"],
    15: [r"Внешн\w*\s+шлюз", r"\bШлюз"],
    16: [r"Сетева\w*\s+экосистем", r"Сетев\w*\s+экосистем"],
    17: [r"Правозащит"],
}

RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_article(path: Path):
    text = path.read_text(encoding="utf-8")
    m = RE_FRONTMATTER.match(text)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    body = text[m.end():].strip()
    # Отсечём хвостовые backlinks/outgoing блоки
    body = re.split(r"\n## (?:Ссылается на|Упоминается в)\n", body)[0].strip()
    try:
        fm["book"] = int(fm.get("book", 0))
        fm["part"] = int(fm.get("part", 0))
        fm["order"] = int(fm.get("order", 0))
    except (ValueError, TypeError):
        return None
    return fm, body


def make_snippet(body: str, match_start: int, match_end: int, width: int = 90) -> str:
    start = max(0, match_start - width)
    end = min(len(body), match_end + width)
    snippet = body[start:end].replace("\n", " ").strip()
    if start > 0:
        snippet = "… " + snippet
    if end < len(body):
        snippet = snippet + " …"
    return snippet


def main() -> int:
    if not CHARTER.exists():
        print(f"[ERR] нет {CHARTER}")
        return 1

    print(f"Читаем: {CHARTER}")
    files = sorted(CHARTER.glob("kniga-*/*.md"))
    print(f"Файлов: {len(files)}")

    # Компилируем регексы
    compiled: dict[int, re.Pattern] = {}
    for id_, pats in PATTERNS.items():
        combined = "|".join(f"(?:{p})" for p in pats)
        compiled[id_] = re.compile(combined)

    # Собираем упоминания
    mentions: dict[int, list[dict]] = {i: [] for i in range(1, 18)}

    for path in files:
        parsed = parse_article(path)
        if not parsed:
            continue
        fm, body = parsed

        # Пропускаем статьи 4.X — там сами описания направлений
        number = fm.get("number", "")
        if number.startswith("4.") and fm.get("book") == 1:
            continue

        for id_, rx in compiled.items():
            for m in rx.finditer(body):
                snippet = make_snippet(body, m.start(), m.end())
                mentions[id_].append({
                    "book": fm["book"],
                    "number": fm["number"],
                    "title": fm.get("title", ""),
                    "snippet": snippet,
                })
                break  # одно упоминание на статью — чтобы не дублировать

    # Дедуплицируем (book, number) внутри каждого направления
    for id_ in mentions:
        seen = set()
        unique = []
        for m in mentions[id_]:
            key = (m["book"], m["number"])
            if key in seen:
                continue
            seen.add(key)
            unique.append(m)
        unique.sort(key=lambda x: (x["book"], x["number"]))
        mentions[id_] = unique[:50]

    if "--dry-run" not in sys.argv:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(
            json.dumps(mentions, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[write] {OUT.relative_to(ROOT)}")
    else:
        print(f"[dry]   {OUT.relative_to(ROOT)}")

    print()
    print("── Упоминаний по направлениям ──")
    for id_ in range(1, 18):
        print(f"  {id_:>2}: {len(mentions[id_])}")
    print()
    print(f"Всего статей со ссылками: {sum(len(v) for v in mentions.values())}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())