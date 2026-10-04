#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 9: правка поиска.

1. Убирает postbuild из package.json (astro-pagefind уже всё делает).
2. Выносит <Search /> из <nav> в BaseLayout.astro.

Запуск:
    python scripts\step_09_fix_search.py --dry-run
    python scripts\step_09_fix_search.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

PKG = ROOT / "package.json"
LAYOUT = ROOT / "src" / "layouts" / "BaseLayout.astro"


def fix_package_json() -> bool:
    if not PKG.exists():
        print(f"[ERR] нет {PKG}")
        return False

    try:
        data = json.loads(PKG.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERR] package.json не читается: {e}")
        return False

    scripts = data.get("scripts", {})
    if "postbuild" not in scripts:
        print("[skip] package.json: postbuild уже убран")
        return False

    if DRY_RUN:
        print("[dry]  package.json: удалить postbuild")
        return True

    del scripts["postbuild"]
    data["scripts"] = scripts
    PKG.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("[fix]  package.json: postbuild удалён")
    return True


def fix_base_layout() -> bool:
    if not LAYOUT.exists():
        print(f"[ERR] нет {LAYOUT}")
        return False

    text = LAYOUT.read_text(encoding="utf-8")

    # Ищем блок nav
    m = re.search(
        r'(<nav class="site-nav"[^>]*>)(.*?)(</nav>)',
        text,
        re.DOTALL,
    )
    if not m:
        print("[warn] не найден <nav class='site-nav'>")
        return False

    nav_body = m.group(2)
    if "<Search />" not in nav_body:
        print("[skip] BaseLayout: <Search /> не внутри <nav>")
        return False

    # Убираем <Search /> из nav
    new_nav_body = re.sub(r"\s*<Search\s*/>\s*", "\n", nav_body)
    new_nav = m.group(1) + new_nav_body.rstrip() + "\n        " + m.group(3)

    # Вставляем <Search /> ПЕРЕД nav
    replacement = "        <Search />\n        " + new_nav
    new_text = text[:m.start()] + replacement + text[m.end():]

    if DRY_RUN:
        print("[dry]  BaseLayout: <Search /> вынести из <nav>")
        return True

    LAYOUT.write_text(new_text, encoding="utf-8")
    print("[fix]  BaseLayout: <Search /> вынесен из <nav>")
    return True


def main() -> int:
    print(f"Проект: {ROOT}")
    if DRY_RUN:
        print("Режим:  --dry-run")
    print()

    print("── 1. package.json ──")
    fix_package_json()
    print()

    print("── 2. BaseLayout.astro ──")
    fix_base_layout()
    print()

    print("Дальше:")
    print("  1. npm install  (обновить node_modules)")
    print("  2. npm run build")
    print("  3. npm run preview")
    print("  4. Открой http://localhost:4321/hartia/")
    print("     Кнопка поиска должна быть СПРАВА ОТ навигации,")
    print("     перед бургером на мобильных.")
    print("  5. git add . && git commit -m 'Fix search layout' && git push")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())