#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 13: улучшение сбора упоминаний.

1. В step_11_direction_mentions.py:
   - увеличивает кэп упоминаний с 30 до 50
   - расширяет стемы для направления 2 (Здравие)
2. Перезапускает сбор.

Запуск:
    python scripts\step_13_mentions_tune.py
    python scripts\step_13_mentions_tune.py --dry-run
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEP11 = ROOT / "scripts" / "step_11_direction_mentions.py"
DRY_RUN = "--dry-run" in sys.argv

# ─── Патч 1: кэп упоминаний 30 → 50 ───
OLD_CAP = "mentions[id_] = unique[:30]"
NEW_CAP = "mentions[id_] = unique[:50]"

# ─── Патч 2: расширенные стемы для Здравия ───
OLD_ZDR = '    2:  [r"\\bЗдрави[еяюи]"],'
NEW_ZDR = (
    '    2:  [\n'
    '        r"\\bЗдрави[еяюи]",\n'
    '        r"\\bЗдоров",\n'
    '        r"\\bМедицин",\n'
    '        r"\\bЛечен",\n'
    '        r"\\bДиагност",\n'
    '        r"\\bРеабилитац",\n'
    '    ],'
)

PATCHES = [
    (OLD_CAP, NEW_CAP, "кэп упоминаний 30 → 50"),
    (OLD_ZDR, NEW_ZDR, "стемы для Здравия расширены"),
]


def apply_patches() -> int:
    if not STEP11.exists():
        print(f"[ERR] нет {STEP11}")
        return 0

    text = STEP11.read_text(encoding="utf-8")
    applied = 0

    for old, new, label in PATCHES:
        if new in text:
            print(f"[skip]  {label} (уже применён)")
            continue
        if old not in text:
            print(f"[warn]  {label}: якорь не найден")
            print(f"        искали: {old!r}")
            continue
        if DRY_RUN:
            print(f"[dry]   {label}")
            continue
        text = text.replace(old, new, 1)
        print(f"[patch] {label}")
        applied += 1

    if applied and not DRY_RUN:
        STEP11.write_text(text, encoding="utf-8")

    return applied


def rerun_step11() -> bool:
    if DRY_RUN:
        print("[dry]   перезапуск step_11_direction_mentions.py")
        return True

    print()
    print("── Перезапуск step_11 ──")
    result = subprocess.run(
        [sys.executable, str(STEP11)],
        cwd=str(ROOT),
        text=True,
    )
    return result.returncode == 0


def main() -> int:
    print(f"Проект: {ROOT}")
    if DRY_RUN:
        print("Режим:  --dry-run")
    print()

    print("── Патчи step_11 ──")
    n = apply_patches()
    print()

    if not rerun_step11():
        print("[ERR] step_11 упал с ошибкой")
        return 1

    print()
    print("Готово. Проверь обновлённый JSON:")
    print(f"  {ROOT / 'src' / 'data' / 'direction-mentions.json'}")
    print()
    print("И страницы направлений:")
    print("  npm run dev")
    print("  http://localhost:4321/hartia/napravleniya/zdravie")
    print("  http://localhost:4321/hartia/napravleniya/noologiya")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())