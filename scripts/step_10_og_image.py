#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 10: OG-картинка для соцсетей.

1. Конвертирует scripts/og_template.svg → public/og-image.png
2. Патчит src/layouts/BaseLayout.astro — добавляет og:image, twitter:image и др.

Зависимость:
    pip install cairosvg

Запуск:
    python scripts\step_10_og_image.py --dry-run
    python scripts\step_10_og_image.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "scripts" / "og_template.svg"
PNG = ROOT / "public" / "og-image.png"
LAYOUT = ROOT / "src" / "layouts" / "BaseLayout.astro"
DRY_RUN = "--dry-run" in sys.argv
FORCE = "--force" in sys.argv

OG_URL = "https://vamhana.github.io/hartia/og-image.png"

# ─── Патч BaseLayout ───
# Якорь: конец блока Twitter
ANCHOR = '<meta name="twitter:description" content={description} />'

OG_TAGS = '''\
    <meta name="twitter:description" content={description} />

    <!-- OG image -->
    <meta property="og:image" content={`${SITE_URL}/og-image.png`} />
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Хартия 5.0 — Протокол Цивилизации Будущего" />

    <meta name="twitter:image" content={`${SITE_URL}/og-image.png`} />
    <meta name="twitter:image:alt" content="Хартия 5.0 — Протокол Цивилизации Будущего" />'''


def convert_svg_to_png() -> bool:
    if not SVG.exists():
        print(f"[ERR] нет {SVG}")
        return False

    if PNG.exists() and not FORCE:
        size_kb = PNG.stat().st_size / 1024
        print(f"[skip]  {PNG.name} уже существует ({size_kb:.1f} КБ). --force для перезаписи.")
        return True

    try:
        import cairosvg
    except ImportError:
        print("[ERR] нет библиотеки cairosvg.")
        print("      Установи: pip install cairosvg")
        print("      Или сконвертируй SVG в PNG онлайн: https://svgtopng.com/")
        print(f"      Размер: 1200×630, сохранить как public/og-image.png")
        return False

    if DRY_RUN:
        print(f"[dry]   {SVG.name} → {PNG.name}")
        return True

    try:
        cairosvg.svg2png(
            url=str(SVG),
            write_to=str(PNG),
            output_width=1200,
            output_height=630,
        )
        size_kb = PNG.stat().st_size / 1024
        print(f"[write] {PNG.name} ({size_kb:.1f} КБ)")
        return True
    except Exception as e:
        print(f"[ERR] ошибка конвертации: {e}")
        print("      Попробуй онлайн: https://svgtopng.com/")
        return False


def patch_layout() -> bool:
    if not LAYOUT.exists():
        print(f"[ERR] нет {LAYOUT}")
        return False

    text = LAYOUT.read_text(encoding="utf-8")

    # Проверка: уже применён?
    if "og:image" in text and "og-image.png" in text:
        print("[skip]  BaseLayout.astro: og:image уже добавлен")
        return True

    if ANCHOR not in text:
        print(f"[warn]  якорь не найден в BaseLayout.astro")
        print(f"        искали: {ANCHOR!r}")
        return False

    if DRY_RUN:
        print("[dry]   BaseLayout.astro: добавить og:image и twitter:image")
        return True

    new_text = text.replace(ANCHOR, OG_TAGS, 1)
    LAYOUT.write_text(new_text, encoding="utf-8")
    print("[patch] BaseLayout.astro: og:image и twitter:image")
    return True


def main() -> int:
    print(f"Проект: {ROOT}")
    if DRY_RUN:
        print("Режим:  --dry-run")
    if FORCE:
        print("Режим:  --force")
    print()

    print("── 1. Конвертация SVG → PNG ──")
    ok_png = convert_svg_to_png()
    print()

    print("── 2. Патч BaseLayout.astro ──")
    ok_layout = patch_layout()
    print()

    if ok_png and ok_layout:
        print("Готово.")
        print()
        print("Проверь локально:")
        print("  npm run dev")
        print("  Открой http://localhost:4321/hartia/og-image.png")
        print("  Должна показаться картинка с цитатой.")
        print()
        print("Затем пуш:")
        print("  git add .")
        print("  git commit -m \"Add OG image for social previews\"")
        print("  git push")
        print()
        print("Проверка превью (после деплоя):")
        print("  https://www.opengraph.xyz/url/https%3A%2F%2Fvamhana.github.io%2Fhartia%2F")
        print("  или просто кинь ссылку в Telegram — превью появится само.")
    else:
        print("Что-то не получилось. Смотри сообщения выше.")
    return 0


if __name__ == "__main__":
    sys.exit(main())