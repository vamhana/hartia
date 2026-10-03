#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 5: исправление навигации и ссылок.

1. index.astro — ссылки на книги через /charter/
2. CharterNav.astro — выезжающая панель на мобильных
3. Заглушки /napravleniya и /soobschestva

Запуск:
    python scripts/step_05_fix_nav.py --dry-run
    python scripts/step_05_fix_nav.py
    python scripts/step_05_fix_nav.py --force
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

FILES: dict[str, str] = {}
PATCHES: list[tuple[Path, str, str, str]] = []

# ═════════════════════════════════════════════════════════════════════════
# 1. CharterNav.astro — выезжающая панель на мобильных
# ═════════════════════════════════════════════════════════════════════════
FILES["src/components/CharterNav.astro"] = """\
---
interface NavArticle {
  number: string;
  title: string;
  part: number;
  partTitle: string;
  slug: string;
  href: string;
  isCurrent: boolean;
}

interface Props {
  book: number;
  bookTitle: string;
  bookHref: string;
  articles: NavArticle[];
}

const { book, bookTitle, bookHref, articles } = Astro.props;

const byPart: Record<number, { partTitle: string; items: NavArticle[] }> = {};
for (const a of articles) {
  if (!byPart[a.part]) {
    byPart[a.part] = { partTitle: a.partTitle, items: [] };
  }
  byPart[a.part].items.push(a);
}

const parts = Object.keys(byPart)
  .map(Number)
  .sort((a, b) => a - b);
---

<button class="charter-nav__toggle" data-nav-toggle aria-label="Открыть оглавление">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
    <line x1="3" y1="6" x2="21" y2="6"/>
    <line x1="3" y1="12" x2="21" y2="12"/>
    <line x1="3" y1="18" x2="21" y2="18"/>
  </svg>
  <span class="mono">Оглавление</span>
</button>

<aside class="charter-nav" data-charter-nav>
  <button class="charter-nav__close" data-nav-close aria-label="Закрыть">×</button>

  <a href={bookHref} class="charter-nav__book">
    <span class="charter-nav__book-label mono">Книга {book}</span>
    <span class="charter-nav__book-title">{bookTitle}</span>
  </a>

  <nav class="charter-nav__toc">
    {parts.map((partNum) => {
      const group = byPart[partNum];
      return (
        <section class="charter-nav__part">
          <h3 class="charter-nav__part-title">
            <span class="mono">Часть {partNum}.</span> {group.partTitle}
          </h3>
          <ul class="charter-nav__list">
            {group.items.map((a) => (
              <li>
                <a
                  href={a.href}
                  class:list={[
                    'charter-nav__link',
                    { 'is-current': a.isCurrent },
                  ]}
                >
                  <span class="charter-nav__num mono">{a.number}</span>
                  <span class="charter-nav__title">{a.title}</span>
                </a>
              </li>
            ))}
          </ul>
        </section>
      );
    })}
  </nav>
</aside>

<script>
  const toggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-charter-nav]');
  const close = document.querySelector('[data-nav-close]');

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    });
  }

  if (close && nav) {
    close.addEventListener('click', () => {
      nav.classList.remove('is-open');
      document.body.style.overflow = '';
    });
  }

  nav?.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => {
      nav.classList.remove('is-open');
      document.body.style.overflow = '';
    });
  });
</script>

<style>
  .charter-nav__toggle {
    display: none;
    align-items: center;
    gap: 0.6rem;
    padding: 0.75rem 1rem;
    margin-bottom: 1.5rem;
    border: 1px solid var(--gold-dim);
    background: var(--bg-raised);
    color: var(--gold);
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all var(--transition);
    border-radius: 2px;
  }

  .charter-nav__toggle:hover {
    border-color: var(--gold);
    background: var(--bg-subtle);
  }

  .charter-nav__close {
    display: none;
    position: absolute;
    top: 1rem;
    right: 1rem;
    width: 2.5rem;
    height: 2.5rem;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: var(--text-secondary);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: color var(--transition);
    z-index: 10;
  }

  .charter-nav__close:hover { color: var(--gold-bright); }

  .charter-nav {
    position: sticky;
    top: 5rem;
    max-height: calc(100vh - 6rem);
    overflow-y: auto;
    padding-right: 1rem;
    border-right: 1px solid var(--gold-dim);
  }

  .charter-nav__book {
    display: block;
    padding-bottom: 1.25rem;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid var(--gold-dim);
    transition: color var(--transition);
  }

  .charter-nav__book:hover { color: var(--gold-bright); }

  .charter-nav__book-label {
    display: block;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--gold);
    margin-bottom: 0.35rem;
  }

  .charter-nav__book-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    line-height: 1.2;
    color: var(--text-primary);
  }

  .charter-nav__toc {
    display: grid;
    gap: 1.75rem;
  }

  .charter-nav__part-title {
    font-family: var(--font-body);
    font-weight: 400;
    font-size: 0.8rem;
    line-height: 1.4;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .charter-nav__part-title .mono {
    color: var(--gold-dim);
    font-size: 0.7rem;
  }

  .charter-nav__list {
    list-style: none;
    display: grid;
    gap: 0.15rem;
  }

  .charter-nav__link {
    display: grid;
    grid-template-columns: 2.5rem 1fr;
    gap: 0.5rem;
    padding: 0.4rem 0.5rem;
    font-size: 0.88rem;
    line-height: 1.35;
    color: var(--text-secondary);
    border-left: 2px solid transparent;
    transition: all var(--transition);
    border-radius: 2px;
  }

  .charter-nav__link:hover {
    color: var(--text-primary);
    background: var(--bg-subtle);
  }

  .charter-nav__link.is-current {
    color: var(--gold-bright);
    background: var(--bg-subtle);
    border-left-color: var(--gold);
  }

  .charter-nav__num {
    color: var(--gold-dim);
    font-size: 0.7rem;
    padding-top: 0.2rem;
  }

  .charter-nav__link.is-current .charter-nav__num {
    color: var(--gold);
  }

  @media (max-width: 960px) {
    .charter-nav__toggle { display: inline-flex; }

    .charter-nav {
      position: fixed;
      top: 0;
      left: 0;
      bottom: 0;
      width: min(85vw, 360px);
      max-height: none;
      padding: 4rem 1.5rem 2rem;
      background: var(--bg-deep);
      border-right: 1px solid var(--gold-dim);
      transform: translateX(-100%);
      transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 100;
      overflow-y: auto;
    }

    .charter-nav.is-open { transform: translateX(0); }

    .charter-nav__close { display: flex; }

    .charter-nav__book { padding-top: 0.5rem; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. Заглушка /napravleniya
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/napravleniya.astro"] = """\
---
import BaseLayout from '../layouts/BaseLayout.astro';
import '../styles/global.css';

const title = 'Направления';
const description = 'Семнадцать направлений цивилизации. Раздел в разработке.';
---

<BaseLayout title={title} description={description}>
  <section class="placeholder">
    <div class="container prose">
      <p class="mono">Раздел в разработке</p>
      <h1>Направления</h1>
      <p>
        Здесь появится Атлас — карта всех семнадцати направлений
        цивилизации, с описаниями, зонами ответственности и связями.
      </p>
      <p>Пока этот раздел в работе. Возвращайтесь — скоро.</p>
      <p><a href={`${import.meta.env.BASE_URL.replace(/\\/$/, '')}/`}>← На главную</a></p>
    </div>
  </section>
</BaseLayout>

<style>
  .placeholder {
    padding-block: 6rem 5rem;
    text-align: center;
  }
  .placeholder .mono { color: var(--gold); margin-bottom: 1.5rem; }
  .placeholder h1 { margin-bottom: 2rem; }
  .placeholder p { color: var(--text-secondary); }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 3. Заглушка /soobschestva
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/soobschestva.astro"] = """\
---
import BaseLayout from '../layouts/BaseLayout.astro';
import '../styles/global.css';

const title = 'Сообщества';
const description = 'Сеть сообществ Хартии. Раздел в разработке.';
---

<BaseLayout title={title} description={description}>
  <section class="placeholder">
    <div class="container prose">
      <p class="mono">Раздел в разработке</p>
      <h1>Сообщества</h1>
      <p>
        Здесь появится карта сети: аккредитованные общины, узлы
        конвергенции, мосты Потоков между ними.
      </p>
      <p>Пока этот раздел в работе. Возвращайтесь — скоро.</p>
      <p><a href={`${import.meta.env.BASE_URL.replace(/\\/$/, '')}/`}>← На главную</a></p>
    </div>
  </section>
</BaseLayout>

<style>
  .placeholder {
    padding-block: 6rem 5rem;
    text-align: center;
  }
  .placeholder .mono { color: var(--gold); margin-bottom: 1.5rem; }
  .placeholder h1 { margin-bottom: 2rem; }
  .placeholder p { color: var(--text-secondary); }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# PATCHES
# ═════════════════════════════════════════════════════════════════════════
PATCHES.append((
    ROOT / "src" / "pages" / "index.astro",
    "url(`/${book.slug}`)",
    "url(`/charter/${book.slug}`)",
    "index: ссылки на книги через /charter",
))


def apply_files():
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
            print(f"[skip]  {rel}")
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


def apply_patches():
    applied = skipped = 0
    for path, old, new, label in PATCHES:
        if not path.exists():
            print(f"[warn] нет {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if new in text:
            print(f"[skip] {label} (уже применён)")
            skipped += 1
            continue
        if old not in text:
            print(f"[warn] якорь не найден: {label}")
            print(f"       искали: {old!r}")
            continue
        if DRY_RUN:
            print(f"[dry]  {label}")
            continue
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")
        print(f"[patch] {label}")
        applied += 1
    return applied, skipped


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
    print("── Патчи ──")
    p, ps = apply_patches()

    print()
    print(f"Записано: {w}, пропущено: {s}. Патчей: {p}.")
    print()
    print("Дальше:")
    print("  npm run dev")
    print("  Проверить на телефоне (DevTools → Toggle device toolbar):")
    print("    http://localhost:4321/hartia/charter/kniga-1/1-10")
    print("  Кнопка «Оглавление» — выезжающая слева панель.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())