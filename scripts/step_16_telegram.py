#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 16: кнопка Telegram-группы.

Создаёт:
  - src/data/links.ts — константы внешних ссылок
  - src/components/TelegramButton.astro — кнопка

Патчит:
  - src/layouts/BaseLayout.astro — импорт + кнопка в футере

Запуск:
    python scripts\step_16_telegram.py --dry-run
    python scripts\step_16_telegram.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

FILES: dict[str, str] = {}

# ═════════════════════════════════════════════════════════════════════════
# 1. src/data/links.ts
# ═════════════════════════════════════════════════════════════════════════
FILES["src/data/links.ts"] = """\
// Внешние ссылки проекта.
// Заполни TELEGRAM_URL своей ссылкой — кнопка появится в футере.
// Пока пусто — кнопка не показывается.

export const TELEGRAM_URL = 'https://t.me/hartia_5'; // например: 'https://t.me/xartia_chat'
export const TELEGRAM_LABEL = 'Обсудить проект';
export const TELEGRAM_HINT = 'Чат Хартии 5.0 в Telegram';
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. src/components/TelegramButton.astro
# ═════════════════════════════════════════════════════════════════════════
FILES["src/components/TelegramButton.astro"] = """\
---
import { TELEGRAM_URL, TELEGRAM_LABEL, TELEGRAM_HINT } from '../data/links';

const enabled = TELEGRAM_URL && TELEGRAM_URL.startsWith('http');
---

{enabled && (
  <a
    href={TELEGRAM_URL}
    class="tg"
    target="_blank"
    rel="noopener noreferrer"
    title={TELEGRAM_HINT}
  >
    <svg
      class="tg__icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/>
    </svg>
    <span class="tg__label">{TELEGRAM_LABEL}</span>
    <span class="tg__arrow" aria-hidden="true">↗</span>
  </a>
)}

<style>
  .tg {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.7rem 1.2rem;
    margin-top: 1.5rem;
    border: 1px solid var(--gold-dim);
    background: transparent;
    color: var(--gold);
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  .tg:hover {
    border-color: var(--gold);
    color: var(--gold-bright);
    background: var(--bg-subtle);
  }

  .tg__icon {
    flex-shrink: 0;
    transition: transform 250ms;
  }

  .tg:hover .tg__icon {
    transform: translateY(-2px);
  }

  .tg__label {
    white-space: nowrap;
  }

  .tg__arrow {
    color: var(--gold-dim);
    transition: all 250ms;
  }

  .tg:hover .tg__arrow {
    color: var(--gold);
    transform: translate(2px, -2px);
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 3. Патчи BaseLayout.astro
# ═════════════════════════════════════════════════════════════════════════
LAYOUT = ROOT / "src" / "layouts" / "BaseLayout.astro"

PATCH_IMPORT = (
    "import Search from '../components/Search.astro';",
    "import Search from '../components/Search.astro';\n"
    "import TelegramButton from '../components/TelegramButton.astro';",
    "импорт TelegramButton",
)

PATCH_INSERT = (
    "        </p>\n      </div>\n    </footer>",
    "        </p>\n"
    "        <TelegramButton />\n"
    "      </div>\n    </footer>",
    "кнопка в футере",
)


def apply_files() -> tuple[int, int]:
    written = skipped = 0
    for rel, content in FILES.items():
        full = ROOT / rel
        if full.exists() and not FORCE:
            try:
                if full.read_text(encoding="utf-8") == content:
                    print(f"[same]  {rel}")
                    skipped += 1
                    continue
            except Exception:
                pass
            print(f"[skip]  {rel} (существует, --force для перезаписи)")
            skipped += 1
            continue
        if DRY_RUN:
            print(f"[dry]   {rel} ({len(content)} B)")
            continue
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        print(f"[write] {rel} ({len(content)} B)")
        written += 1
    return written, skipped


def apply_patches() -> int:
    if not LAYOUT.exists():
        print(f"[warn]  нет {LAYOUT}")
        return 0

    text = LAYOUT.read_text(encoding="utf-8")
    applied = 0

    for old, new, label in [PATCH_IMPORT, PATCH_INSERT]:
        if new.strip() in text:
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
        LAYOUT.write_text(text, encoding="utf-8")
    return applied


def main() -> int:
    if not ROOT.exists():
        print(f"[ERR] нет {ROOT}")
        return 1

    print(f"Проект: {ROOT}")
    if DRY_RUN: print("Режим: --dry-run")
    if FORCE: print("Режим: --force")
    print()

    print("── Файлы ──")
    w, s = apply_files()
    print()

    print("── Патчи BaseLayout ──")
    p = apply_patches()
    print()

    print(f"Записано: {w}, пропущено: {s}, патчей: {p}.")
    print()
    print("Дальше:")
    print("  1. Создай группу в Telegram.")
    print("  2. Получи ссылку вида https://t.me/xxx")
    print("  3. Открой src/data/links.ts и вставь её в TELEGRAM_URL.")
    print("  4. npm run dev — проверь футер.")
    print("  5. git add . && git commit -m 'Add Telegram button' && git push")
    print()
    print("Пока TELEGRAM_URL пустой — кнопки на сайте не будет.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())