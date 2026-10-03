#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 2: SEO-метатеги, бургер-меню, слоган.

Применяет:
  1. BaseLayout.astro — SEO, OG, JSON-LD, бургер-меню для мобильных.
  2. index.astro — слоган «Цивилизация как открытый код».
  3. public/robots.txt — новый файл.

Запуск:
    python scripts/step_02_seo_nav.py
    python scripts/step_02_seo_nav.py --dry-run
    python scripts/step_02_seo_nav.py --force
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

SITE_TITLE = "Хартия 5.0"
SITE_SUBTITLE = "Протокол Цивилизации Будущего"
SITE_SLOGAN = "Цивилизация как открытый код"
SITE_DESCRIPTION = (
    "Хартия 5.0 — протокол построения планетарной цивилизации, "
    "основанной на развитии, а не накоплении. Сводный регламент, "
    "модульная версия."
)
SITE_URL = "https://vamhana.github.io/hartia"
AUTHOR = "Первый Архитектор"

FILES: dict[str, str] = {}

# ═════════════════════════════════════════════════════════════════════════
# 1. BaseLayout.astro — SEO + бургер-меню
# ═════════════════════════════════════════════════════════════════════════
FILES["src/layouts/BaseLayout.astro"] = """\
---
interface Props {
  title: string;
  description?: string;
}

const {
  title,
  description = 'Хартия 5.0 — протокол построения планетарной цивилизации, основанной на развитии, а не накоплении.',
} = Astro.props;

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const url = (path: string) => `${base}${path.startsWith('/') ? path : `/${path}`}`;

const SITE_TITLE = 'Хартия 5.0';
const SITE_SUBTITLE = 'Протокол Цивилизации Будущего';
const SITE_URL = 'https://vamhana.github.io/hartia';
const AUTHOR = 'Первый Архитектор';

const pageTitle = title === SITE_TITLE
  ? `${SITE_TITLE} — ${SITE_SUBTITLE}`
  : `${title} — ${SITE_TITLE}`;

const canonical = new URL(Astro.url.pathname, SITE_URL).toString();

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Book',
  name: `${SITE_TITLE} — ${SITE_SUBTITLE}`,
  alternateName: 'Xartia 5.0',
  author: { '@type': 'Person', name: AUTHOR },
  inLanguage: 'ru',
  genre: ['Философия', 'Социальная архитектура', 'Футурология'],
  abstract: description,
  url: SITE_URL,
};
---

<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>{pageTitle}</title>
    <meta name="description" content={description} />
    <meta name="author" content={AUTHOR} />
    <meta name="generator" content={Astro.generator} />

    <link rel="canonical" href={canonical} />

    <!-- Open Graph -->
    <meta property="og:type" content="book" />
    <meta property="og:title" content={pageTitle} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    <meta property="og:site_name" content={`${SITE_TITLE} — ${SITE_SUBTITLE}`} />
    <meta property="og:locale" content="ru_RU" />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={pageTitle} />
    <meta name="twitter:description" content={description} />

    <!-- JSON-LD -->
    <script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />

    <link rel="icon" type="image/svg+xml" href={url('/favicon.svg')} />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Spectral:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <header class="site-header">
      <div class="container site-header__inner">
        <a href={url('/')} class="brand">
          <span class="brand__mark" aria-hidden="true">✶</span>
          <span class="brand__text">
            <span class="brand__name">Хартия 5.0</span>
            <span class="brand__sub">Протокол Цивилизации Будущего</span>
          </span>
        </a>

        <button
          class="nav-toggle"
          type="button"
          aria-label="Открыть меню"
          aria-expanded="false"
          aria-controls="site-nav"
        >
          <span></span><span></span><span></span>
        </button>

        <nav class="site-nav" id="site-nav" aria-label="Основная навигация">
          <a href={url('/charter')}>Хартия</a>
          <a href={url('/napravleniya')}>Направления</a>
          <a href={url('/soobschestva')}>Сообщества</a>
          <a href={url('/music')} class="site-nav__music">Музыка</a>
        </nav>
      </div>
    </header>

    <main class="site-main">
      <slot />
    </main>

    <footer class="site-footer">
      <div class="container site-footer__inner">
        <p class="site-footer__quote">
          «Мудрость без действия — это бегство от реальности.
          Действие без мудрости — это хаос.
          А мудрый бунт — высший пилотаж свободы.»
        </p>
        <p class="site-footer__meta">
          <span class="mono">{SITE_TITLE}</span>
          <span class="site-footer__sep">·</span>
          <span>{AUTHOR}</span>
        </p>
      </div>
    </footer>

    <script>
      // Бургер-меню
      const toggle = document.querySelector('.nav-toggle');
      const nav = document.querySelector('.site-nav');
      if (toggle && nav) {
        toggle.addEventListener('click', () => {
          const open = toggle.getAttribute('aria-expanded') === 'true';
          toggle.setAttribute('aria-expanded', String(!open));
          nav.classList.toggle('is-open', !open);
          document.body.style.overflow = !open ? 'hidden' : '';
        });
        nav.querySelectorAll('a').forEach((a) =>
          a.addEventListener('click', () => {
            toggle.setAttribute('aria-expanded', 'false');
            nav.classList.remove('is-open');
            document.body.style.overflow = '';
          })
        );
      }
    </script>
  </body>
</html>

<style>
  .site-header {
    border-bottom: 1px solid var(--gold-dim);
    padding-block: 1rem;
    position: sticky;
    top: 0;
    background: color-mix(in srgb, var(--bg-deep) 92%, transparent);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    z-index: 50;
  }

  .site-header__inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  .brand {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    color: var(--text-primary);
    transition: color var(--transition);
  }

  .brand:hover { color: var(--gold-bright); }

  .brand__mark {
    color: var(--gold);
    font-size: 1.35rem;
    line-height: 1;
    transition: transform var(--transition);
  }

  .brand:hover .brand__mark { transform: rotate(90deg); }

  .brand__text {
    display: flex;
    flex-direction: column;
    line-height: 1.15;
  }

  .brand__name {
    font-family: var(--font-display);
    font-size: 1.25rem;
    font-weight: 500;
    letter-spacing: 0.01em;
  }

  .brand__sub {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 0.1rem;
  }

  .site-nav {
    display: flex;
    gap: 1.75rem;
    font-family: var(--font-mono);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  .site-nav a {
    color: var(--text-secondary);
    transition: color var(--transition);
  }

  .site-nav a:hover { color: var(--gold-bright); }

  .site-nav__music { color: var(--cyan); }
  .site-nav__music:hover { color: var(--gold-bright); }

  .nav-toggle {
    display: none;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
    width: 34px;
    height: 34px;
    padding: 6px;
  }

  .nav-toggle span {
    display: block;
    height: 1px;
    background: var(--gold);
    transition: all var(--transition);
  }

  .nav-toggle[aria-expanded="true"] span:nth-child(1) {
    transform: translateY(6px) rotate(45deg);
  }
  .nav-toggle[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
  .nav-toggle[aria-expanded="true"] span:nth-child(3) {
    transform: translateY(-6px) rotate(-45deg);
  }

  .site-main { flex: 1; }

  .site-footer {
    border-top: 1px solid var(--gold-dim);
    padding-block: 3rem;
    margin-top: 6rem;
    background: var(--bg-raised);
  }

  .site-footer__inner {
    max-width: var(--max-w);
    margin-inline: auto;
    text-align: center;
  }

  .site-footer__quote {
    font-family: var(--font-display);
    font-style: italic;
    font-size: 1.15rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
    line-height: 1.6;
  }

  .site-footer__meta {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-muted);
  }

  .site-footer__sep { margin-inline: 0.6rem; color: var(--gold-dim); }

  @media (max-width: 780px) {
    .nav-toggle { display: flex; }
    .brand__sub { display: none; }

    .site-nav {
      position: fixed;
      inset: 0;
      background: var(--bg-deep);
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 2rem;
      font-size: 1.1rem;
      letter-spacing: 0.2em;
      transform: translateX(100%);
      transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 40;
    }

    .site-nav.is-open { transform: translateX(0); }

    .site-nav a { font-size: 1.1rem; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. index.astro — слоган под эпиграфом
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/index.astro"] = """\
---
import BaseLayout from '../layouts/BaseLayout.astro';
import '../styles/global.css';

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const url = (path: string) => `${base}${path.startsWith('/') ? path : `/${path}`}`;

function plural(n: number, forms: [string, string, string]): string {
  const n10 = n % 10;
  const n100 = n % 100;
  if (n10 === 1 && n100 !== 11) return forms[0];
  if (n10 >= 2 && n10 <= 4 && (n100 < 10 || n100 >= 20)) return forms[1];
  return forms[2];
}

const epigraph = [
  'Мир, в котором мы живём, — тюрьма со своими камерами:',
  'в какой-то лучше, в какой-то хуже.',
  '',
  'У этой тюрьмы два начальника — власть и деньги.',
  'Пока они управляют человеком, он заключён.',
  '',
  'Освобождение начинается с лишения их власти над человеком.',
  'Свобода — это не когда исчезает решётка.',
  'Свобода — когда ты перестаёшь видеть небо сквозь неё.',
];

const books = [
  { num: 'I',    slug: 'kniga-1', title: 'Основы и архитектура',        parts: 6, desc: 'Преамбула, ценности, неизменяемое ядро, направления, ячейки, роли.' },
  { num: 'II',   slug: 'kniga-2', title: 'Процессы и процедуры',        parts: 8, desc: 'Жизненный цикл сигнала, Коннект, План реализации, сбои, избыток.' },
  { num: 'III',  slug: 'kniga-3', title: 'Управление и контроль',       parts: 5, desc: 'Балансировка, Верификация, Жюри, Обнуление, Хранители.' },
  { num: 'IV',   slug: 'kniga-4', title: 'Развитие и самокоррекция',    parts: 7, desc: 'Новые профессии, пятилетний пересмотр, кванты, самообнаружение.' },
  { num: 'V',    slug: 'kniga-5', title: 'Человек, сообщества, мир',    parts: 8, desc: 'Путь участника, мастерство, дети, Шлюз, конвергенция государств.' },
  { num: 'VI',   slug: 'kniga-6', title: 'Экстренные режимы',           parts: 5, desc: 'Красный Контур, Стальной Колокол, Квант оружия, ПТТ, адаптация.' },
  { num: 'VII',  slug: 'kniga-7', title: 'Заключительные положения',    parts: 4, desc: 'Языковой протокол, санкции, порядок изменения, философия.' },
  { num: 'VIII', slug: 'kniga-8', title: 'Экспериментальные протоколы', parts: 2, desc: 'Цифровое ядро Первой сотни. Место для будущего.' },
];
---

<BaseLayout title="Хартия 5.0">
  <section class="hero">
    <div class="container">
      <p class="hero__label">Хартия 5.0 · Сводный регламент · Модульная версия</p>

      <blockquote class="hero__epigraph">
        {epigraph.map((line) =>
          line === ''
            ? <span class="hero__spacer" aria-hidden="true" />
            : <p>{line}</p>
        )}
        <footer class="hero__attribution">— Первый Архитектор</footer>
      </blockquote>

      <p class="hero__slogan">Цивилизация как открытый код</p>

      <div class="hero__actions">
        <a href={url('/charter')} class="btn btn--primary">Читать Хартию</a>
        <a href={url('/music')} class="btn btn--ghost">Слушать музыку бунта →</a>
      </div>
    </div>
  </section>

  <section class="books">
    <div class="container">
      <header class="section-head">
        <span class="section-head__num">VIII</span>
        <h2 class="section-head__title">Книги</h2>
        <p class="section-head__sub">Восемь частей. Двести статей. Один протокол.</p>
      </header>

      <ul class="books__grid">
        {books.map((book) => (
          <li>
            <a href={url(`/${book.slug}`)} class="book-card">
              <span class="book-card__num">{book.num}</span>
              <h3 class="book-card__title">{book.title}</h3>
              <p class="book-card__desc">{book.desc}</p>
              <span class="book-card__meta">
                {book.parts} {plural(book.parts, ['часть', 'части', 'частей'])}
              </span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  </section>

  <section class="manifest">
    <div class="container prose">
      <p class="manifest__lead">
        Мы не создаём общество, в котором проблемы исчезают.
        Мы создаём общество, в котором проблемы не теряются.
      </p>
      <p>
        Хартия не защищает существующую систему от изменений.
        Она защищает механизм её осмысленного изменения.
        Каждые пять лет сама архитектура получает право спросить:
        «Мы всё ещё устроены правильно?» А каждые пятьдесят — более глубокий вопрос:
        «Не слишком ли мы устроены? И не пора ли нам выйти за собственные пределы?»
      </p>
    </div>
  </section>
</BaseLayout>

<style>
  .hero {
    padding-block: 6rem 5rem;
    position: relative;
  }

  .hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 1px;
    height: 3rem;
    background: linear-gradient(to bottom, transparent, var(--gold-dim));
  }

  .hero__label {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    text-align: center;
    margin-bottom: 4rem;
  }

  .hero__epigraph {
    max-width: 42ch;
    margin-inline: auto;
    font-family: var(--font-display);
    font-style: italic;
    font-size: clamp(1.35rem, 2.5vw, 1.75rem);
    line-height: 1.5;
    color: var(--text-primary);
    text-align: center;
  }

  .hero__epigraph p { margin-bottom: 0; }

  .hero__spacer { display: block; height: 1.1em; }

  .hero__attribution {
    margin-top: 2rem;
    font-family: var(--font-mono);
    font-style: normal;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--gold);
  }

  .hero__slogan {
    margin-top: 3rem;
    text-align: center;
    font-family: var(--font-mono);
    font-size: 0.85rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--cyan);
    position: relative;
    padding-top: 2rem;
  }

  .hero__slogan::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 3rem;
    height: 1px;
    background: var(--gold-dim);
  }

  .hero__actions {
    margin-top: 3rem;
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .section-head {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    column-gap: 1.25rem;
    row-gap: 0.25rem;
    align-items: baseline;
    margin-bottom: 3rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--gold-dim);
  }

  .section-head__num {
    grid-row: 1 / 3;
    font-family: var(--font-mono);
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    color: var(--gold);
    padding-top: 0.6rem;
  }

  .section-head__title {
    font-size: clamp(1.75rem, 3vw, 2.5rem);
    margin: 0;
  }

  .section-head__sub {
    font-style: italic;
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin: 0;
  }

  .books { padding-block: 4rem; }

  .books__grid {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }

  .book-card {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 2rem;
    border: 1px solid var(--gold-dim);
    background: var(--bg-raised);
    transition: all var(--transition);
    position: relative;
    overflow: hidden;
  }

  .book-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
    opacity: 0;
    transition: opacity var(--transition);
  }

  .book-card:hover {
    border-color: var(--gold);
    background: var(--bg-subtle);
    transform: translateY(-2px);
  }

  .book-card:hover::before { opacity: 1; }

  .book-card__num {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: var(--gold);
    margin-bottom: 0.75rem;
  }

  .book-card__title {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
    transition: color var(--transition);
  }

  .book-card:hover .book-card__title { color: var(--gold-bright); }

  .book-card__desc {
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 1.5rem;
    flex: 1;
  }

  .book-card__meta {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding-top: 1rem;
    border-top: 1px solid var(--gold-dim);
  }

  .manifest {
    padding-block: 6rem;
    margin-top: 4rem;
    border-top: 1px solid var(--gold-dim);
  }

  .manifest__lead {
    font-family: var(--font-display);
    font-size: clamp(1.5rem, 3vw, 2rem);
    line-height: 1.35;
    color: var(--gold-bright);
    text-align: center;
    margin-bottom: 2.5rem;
    font-style: italic;
  }

  .manifest p:not(.manifest__lead) {
    color: var(--text-secondary);
    font-size: 1.05rem;
  }

  @media (max-width: 720px) {
    .books__grid { grid-template-columns: 1fr; }
    .hero { padding-block: 4rem 3rem; }
    .hero__label { margin-bottom: 2.5rem; }
    .hero__actions { margin-top: 2.5rem; }
    .section-head { grid-template-columns: 1fr; }
    .section-head__num { grid-row: auto; padding-top: 0; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 3. robots.txt
# ═════════════════════════════════════════════════════════════════════════
FILES["public/robots.txt"] = """\
User-agent: *
Allow: /

Sitemap: https://vamhana.github.io/hartia/sitemap-index.xml
"""


def apply() -> tuple[int, int, int]:
    """Возвращает (записано, пропущено, отсутствует)."""
    written = skipped = 0
    for rel, content in FILES.items():
        full = ROOT / rel
        if full.exists() and not FORCE:
            # Проверим, не тот же контент
            try:
                if full.read_text(encoding="utf-8") == content:
                    print(f"[same]  {rel}")
                    skipped += 1
                    continue
            except Exception:
                pass
            print(f"[skip]  {rel} (уже существует, используйте --force)")
            skipped += 1
            continue
        if DRY_RUN:
            print(f"[dry]   {rel} ({len(content)} B)")
            continue
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        print(f"[write] {rel} ({len(content)} B)")
        written += 1
    return written, skipped, 0


def main() -> int:
    if not ROOT.exists():
        print(f"[ERR] нет корня проекта: {ROOT}")
        return 1

    print(f"Проект: {ROOT}")
    if DRY_RUN:
        print("Режим: --dry-run (ничего не будет записано)")
    if FORCE:
        print("Режим: --force (перезапись разрешена)")
    print()

    print("── Файлы ──")
    w, s, _ = apply()

    print()
    print(f"Готово. Записано: {w}, пропущено: {s}.")

    print()
    print("Дальше:")
    print("  npm run dev")
    print("  Открыть http://localhost:4321/hartia/")
    print("  Проверить на телефоне через 'Responsive' в DevTools.")
    print()
    print("  git add .")
    print('  git commit -m "Step 2: SEO, burger nav, slogan"')
    print("  git push")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())