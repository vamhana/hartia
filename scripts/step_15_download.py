#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 15: скачивание Хартии целиком.

Собирает три файла в public/download/:
  - charter.md    — копия README.md
  - charter.txt   — все статьи чистым текстом
  - charter.json  — структурированные данные (314 статей)

Патчит src/pages/charter/index.astro — добавляет блок скачивания.

Запуск:
    python scripts\step_15_download.py --dry-run
    python scripts\step_15_download.py
"""

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CHARTER_SRC = ROOT / "src" / "content" / "charter_original"
if not CHARTER_SRC.exists():
    CHARTER_SRC = ROOT / "src" / "content" / "charter"
OUT_DIR = ROOT / "public" / "download"
INDEX = ROOT / "src" / "pages" / "charter" / "index.astro"

DRY_RUN = "--dry-run" in sys.argv

RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
RE_BACKLINKS = re.compile(r"\n## (?:Ссылается на|Упоминается в)\n")

ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


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
    body = RE_BACKLINKS.split(body)[0].strip()
    try:
        fm["book"] = int(fm.get("book", 0))
        fm["part"] = int(fm.get("part", 0))
        fm["order"] = int(fm.get("order", 0))
    except (ValueError, TypeError):
        return None
    return fm, body


def collect_articles():
    """Возвращает список словарей, отсортированных по книге, части, порядку."""
    files = sorted(CHARTER_SRC.glob("kniga-*/*.md"))
    items = []
    for path in files:
        parsed = parse_article(path)
        if not parsed:
            continue
        fm, body = parsed
        items.append({"fm": fm, "body": body, "path": path})
    items.sort(key=lambda x: (x["fm"]["book"], x["fm"]["order"]))
    return items


def build_txt(items) -> str:
    """Собирает txt-файл."""
    lines = []
    lines.append("ХАРТИЯ 5.0")
    lines.append("Протокол Цивилизации Будущего")
    lines.append("Первый Архитектор")
    lines.append("")
    lines.append("=" * 70)
    lines.append("")

    current_book = None
    current_part = None
    for it in items:
        fm = it["fm"]
        if fm["book"] != current_book:
            current_book = fm["book"]
            current_part = None
            lines.append("")
            lines.append("=" * 70)
            lines.append(f"КНИГА {ROMAN[current_book]}. {fm['bookTitle'].upper()}")
            lines.append("=" * 70)
            lines.append("")

        if fm["part"] != current_part:
            current_part = fm["part"]
            lines.append("")
            lines.append(f"--- Часть {current_part}. {fm['partTitle']} ---")
            lines.append("")

        lines.append("")
        lines.append(f"Статья {fm['number']}. {fm['title']}")
        if fm.get("source"):
            lines.append(f"({fm['source']})")
        lines.append("")
        lines.append(it["body"])
        lines.append("")

    return "\n".join(lines)


def build_json(items) -> dict:
    """Собирает json с полной структурой."""
    books: dict[int, dict] = {}
    for it in items:
        fm = it["fm"]
        b = fm["book"]
        if b not in books:
            books[b] = {
                "number": b,
                "roman": ROMAN[b],
                "title": fm["bookTitle"],
                "parts": {},
            }
        p = fm["part"]
        if p not in books[b]["parts"]:
            books[b]["parts"][p] = {
                "number": p,
                "title": fm["partTitle"],
                "articles": [],
            }
        books[b]["parts"][p]["articles"].append({
            "number": fm["number"],
            "title": fm["title"],
            "source": fm.get("source", ""),
            "order": fm["order"],
            "body": it["body"],
        })

    return {
        "title": "Хартия 5.0",
        "subtitle": "Протокол Цивилизации Будущего",
        "author": "Первый Архитектор",
        "language": "ru",
        "articles_total": len(items),
        "books": [
            {
                **books[b],
                "parts": sorted(books[b]["parts"].values(), key=lambda p: p["number"]),
            }
            for b in sorted(books.keys())
        ],
    }


def write_files(items) -> int:
    if DRY_RUN:
        print(f"[dry]   {OUT_DIR.relative_to(ROOT)}/charter.md")
        print(f"[dry]   {OUT_DIR.relative_to(ROOT)}/charter.txt")
        print(f"[dry]   {OUT_DIR.relative_to(ROOT)}/charter.json")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0

    # 1. markdown — копия README
    if README.exists():
        shutil.copy2(README, OUT_DIR / "charter.md")
        size_kb = (OUT_DIR / "charter.md").stat().st_size / 1024
        print(f"[write] charter.md ({size_kb:.1f} КБ)")
        written += 1
    else:
        print(f"[warn]  {README} не найден — charter.md не создан")

    # 2. txt
    txt = build_txt(items)
    (OUT_DIR / "charter.txt").write_text(txt, encoding="utf-8")
    size_kb = (OUT_DIR / "charter.txt").stat().st_size / 1024
    print(f"[write] charter.txt ({size_kb:.1f} КБ)")
    written += 1

    # 3. json
    data = build_json(items)
    (OUT_DIR / "charter.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    size_kb = (OUT_DIR / "charter.json").stat().st_size / 1024
    print(f"[write] charter.json ({size_kb:.1f} КБ)")
    written += 1

    return written


# ─── Патч /charter/index.astro ───
DOWNLOAD_BLOCK = '''
  <section class="download">
    <div class="container">
      <header class="section-head">
        <span class="section-head__num mono">↓</span>
        <h2 class="section-head__title">Скачать Хартию целиком</h2>
        <p class="section-head__sub">
          Протокол Цивилизации Будущего — в удобном формате для чтения,
          работы или архива.
        </p>
      </header>

      <ul class="download__grid">
        <li>
          <a href={url('/download/charter.txt')} class="download__item" download>
            <span class="download__icon mono">.txt</span>
            <span class="download__name">Простой текст</span>
            <span class="download__desc">
              314 статей в одном файле. Для блокнота, Kindle, чтения без разметки.
            </span>
          </a>
        </li>
        <li>
          <a href={url('/download/charter.md')} class="download__item" download>
            <span class="download__icon mono">.md</span>
            <span class="download__name">Markdown</span>
            <span class="download__desc">
              Исходник с разметкой. Для Obsidian, VSCode, любого редактора.
            </span>
          </a>
        </li>
        <li>
          <a href={url('/download/charter.json')} class="download__item" download>
            <span class="download__icon mono">.json</span>
            <span class="download__name">JSON</span>
            <span class="download__desc">
              Структурированные данные: книги, части, статьи. Для анализа и разработки.
            </span>
          </a>
        </li>
      </ul>

      <p class="download__license mono">
        Лицензия: CC BY-SA 4.0 · Свободно копируйте, изменяйте, распространяйте
      </p>
    </div>
  </section>

<style>
  .download {
    padding-block: 4rem;
    margin-top: 3rem;
    border-top: 1px solid var(--gold-dim);
  }

  .section-head {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    column-gap: 1.25rem;
    row-gap: 0.25rem;
    align-items: baseline;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--gold-dim);
  }

  .section-head__num {
    grid-row: 1 / 3;
    padding-top: 0.6rem;
    color: var(--gold);
    font-size: 0.9rem;
  }

  .section-head__title { margin: 0; font-size: clamp(1.6rem, 3vw, 2.25rem); }

  .section-head__sub {
    font-style: italic;
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin: 0;
  }

  .download__grid {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin-bottom: 2.5rem;
  }

  .download__item {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1.75rem;
    border: 1px solid var(--gold-dim);
    background: var(--bg-raised);
    transition: all 250ms;
    height: 100%;
  }

  .download__item:hover {
    border-color: var(--gold);
    background: var(--bg-subtle);
    transform: translateY(-2px);
  }

  .download__icon {
    font-size: 1.5rem;
    color: var(--gold);
    font-weight: 500;
    letter-spacing: 0.05em;
  }

  .download__name {
    font-family: var(--font-display);
    font-size: 1.35rem;
    color: var(--text-primary);
    transition: color 200ms;
  }

  .download__item:hover .download__name { color: var(--gold-bright); }

  .download__desc {
    font-size: 0.92rem;
    color: var(--text-secondary);
    line-height: 1.5;
    flex: 1;
  }

  .download__license {
    text-align: center;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  @media (max-width: 720px) {
    .download__grid { grid-template-columns: 1fr; }
    .section-head { grid-template-columns: 1fr; }
    .section-head__num { grid-row: auto; padding-top: 0; }
  }
</style>
'''


def patch_index() -> bool:
    if not INDEX.exists():
        print(f"[warn]  {INDEX} не найден")
        return False

    text = INDEX.read_text(encoding="utf-8")

    if "download__grid" in text:
        print("[skip]  index.astro: блок скачивания уже добавлен")
        return True

    # Вставляем перед </BaseLayout>
    anchor = "</BaseLayout>"
    if anchor not in text:
        print(f"[warn]  якорь '{anchor}' не найден в index.astro")
        return False

    if DRY_RUN:
        print("[dry]   index.astro: вставить блок скачивания")
        return True

    new_text = text.replace(anchor, DOWNLOAD_BLOCK + "\n" + anchor, 1)
    INDEX.write_text(new_text, encoding="utf-8")
    print("[patch] index.astro: блок скачивания добавлен")
    return True


def main() -> int:
    if not CHARTER_SRC.exists():
        print(f"[ERR] нет {CHARTER_SRC}")
        return 1

    print(f"Проект: {ROOT}")
    print(f"Источник: {CHARTER_SRC.relative_to(ROOT)}")
    if DRY_RUN: print("Режим: --dry-run")
    print()

    items = collect_articles()
    print(f"Найдено статей: {len(items)}")
    print()

    print("── Файлы скачивания ──")
    write_files(items)
    print()

    print("── Патч /charter ──")
    patch_index()
    print()

    print("Проверь:")
    print("  npm run dev")
    print("  http://localhost:4321/hartia/download/charter.txt")
    print("  http://localhost:4321/hartia/download/charter.json")
    print("  http://localhost:4321/hartia/charter  (блок внизу)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())