#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 6: Интеграция GoatCounter.

Добавляет скрипт аналитики в BaseLayout.astro.
Скрипт работает только в продакшене, чтобы не засорять статистику при разработке.

Запуск:
    python scripts/step_06_goatcounter.py --dry-run
    python scripts/step_06_goatcounter.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_LAYOUT = ROOT / "src" / "layouts" / "BaseLayout.astro"

# --- НАСТРОЙКИ ---
SITE_CODE = "vamhana"  # <-- ЗАМЕНИТЕ на ваш код сайта из GoatCounter
# -----------------

# Скрипт, который будет добавлен в <head>
GOATCOUNTER_SCRIPT = f'''
    <!-- GoatCounter Analytics -->
    {{import.meta.env.PROD && (
      <script
        data-goatcounter="https://{SITE_CODE}.goatcounter.com/count"
        async
        src="//gc.zgo.at/count.js"
      ></script>
    )}}
'''

PATCHES = [
    (
        BASE_LAYOUT,
        "    <link rel=\"icon\"",
        GOATCOUNTER_SCRIPT + "\n    <link rel=\"icon\"",
        "BaseLayout: добавлен скрипт GoatCounter",
    ),
]

def apply():
    if not BASE_LAYOUT.exists():
        print(f"[ERR] Не найден {BASE_LAYOUT}")
        return

    print(f"Проект: {ROOT}")
    text = BASE_LAYOUT.read_text(encoding="utf-8")

    for path, anchor, insertion, label in PATCHES:
        if insertion.strip() in text:
            print(f"[skip] {label} (уже применен)")
            continue
        if anchor not in text:
            print(f"[warn] Якорь не найден: {label}")
            print(f"       Искали: {anchor!r}")
            continue

        text = text.replace(anchor, insertion, 1)
        path.write_text(text, encoding="utf-8")
        print(f"[patch] {label}")

    print("\nДальше:")
    print("  1. npm run dev")
    print("  2. Откройте сайт в браузере (в режиме `npm run dev` скрипт не выполняется).")
    print("  3. Проверьте работу аналитики на продакшене после пуша.")
    print("     Откройте https://vamhana.github.io/hartia/ и зайдите в панель GoatCounter.")

if __name__ == "__main__":
    apply()