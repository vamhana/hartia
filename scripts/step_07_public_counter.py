#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 7: Публичный счётчик посещений в футере.

Добавляет в BaseLayout.astro блок с числом визитов,
получаемым через API GoatCounter.

Запуск:
    python scripts/step_07_public_counter.py --dry-run
    python scripts/step_07_public_counter.py
    python scripts/step_07_public_counter.py --force
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

SITE_CODE = "vamhana"
BASE_LAYOUT = ROOT / "src" / "layouts" / "BaseLayout.astro"

# ─── Что добавляем ───
# 1. Строка со счётчиком в футере, после существующего meta
FOOTER_COUNTER = """\
          <span class="site-footer__sep">·</span>
          <span
            class="site-footer__counter"
            data-visit-counter
            aria-live="polite"
          ></span>"""

# 2. Скрипт перед закрывающим </body> или после бургер-меню
COUNTER_SCRIPT = f"""\
    <script>
      // Публичный счётчик посещений GoatCounter
      (function () {{
        const el = document.querySelector('[data-visit-counter]');
        if (!el) return;
        fetch('https://{SITE_CODE}.goatcounter.com/counter/TOTAL.json')
          .then((r) => (r.ok ? r.json() : null))
          .then((d) => {{
            if (!d || !d.count) return;
            el.textContent = `визитов: ${{d.count}}`;
          }})
          .catch(() => {{}});
      }})();
    </script>"""

# 3. CSS для счётчика
COUNTER_CSS = """\

  .site-footer__counter {
    color: var(--cyan);
    font-variant-numeric: tabular-nums;
  }"""

PATCHES = [
    (
        BASE_LAYOUT,
        '          <span>{AUTHOR}</span>\n        </p>',
        '          <span>{AUTHOR}</span>\n' + FOOTER_COUNTER + '\n        </p>',
        "BaseLayout: строка счётчика в футере",
    ),
    (
        BASE_LAYOUT,
        "  </body>\n</html>",
        COUNTER_SCRIPT + "\n  </body>\n</html>",
        "BaseLayout: скрипт получения счётчика",
    ),
    (
        BASE_LAYOUT,
        "  .site-footer__sep { margin-inline: 0.6rem; color: var(--gold-dim); }",
        "  .site-footer__sep { margin-inline: 0.6rem; color: var(--gold-dim); }"
        + COUNTER_CSS,
        "BaseLayout: стиль счётчика",
    ),
]


def apply() -> int:
    if not BASE_LAYOUT.exists():
        print(f"[ERR] нет {BASE_LAYOUT}")
        return 1

    print(f"Проект: {ROOT}")
    if DRY_RUN: print("Режим: --dry-run")
    if FORCE: print("Режим: --force")
    print()

    text = BASE_LAYOUT.read_text(encoding="utf-8")
    applied = 0

    for _, anchor, replacement, label in PATCHES:
        if replacement.strip() in text:
            print(f"[skip]  {label} (уже применён)")
            continue
        if anchor not in text:
            print(f"[warn]  {label}: якорь не найден")
            print(f"        искали: {anchor!r}")
            continue
        if DRY_RUN:
            print(f"[dry]   {label}")
            continue
        text = text.replace(anchor, replacement, 1)
        print(f"[patch] {label}")
        applied += 1

    if applied and not DRY_RUN:
        BASE_LAYOUT.write_text(text, encoding="utf-8")

    print()
    print(f"Патчей применено: {applied}.")
    print()
    print("Дальше:")
    print("  1. Включи в GoatCounter: Settings → Allow adding visitor counts")
    print("  2. npm run dev  (счётчик не заработает локально — он в PROD)")
    print("  3. git add . && git commit -m 'Public visit counter' && git push")
    print("  4. Через 2 минуты открой https://vamhana.github.io/hartia/")
    print("     В футере появится «визитов: N»")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(apply())