#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 4: страницы Хартии.

Создаёт:
  - src/content.config.ts (обновляет, добавляет charter)
  - src/components/CharterNav.astro
  - src/pages/charter/index.astro
  - src/pages/charter/[book]/index.astro
  - src/pages/charter/[book]/[article].astro

Запуск:
    python scripts/step_04_charter_pages.py --dry-run
    python scripts/step_04_charter_pages.py
    python scripts/step_04_charter_pages.py --force
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

FILES: dict[str, str] = {}

# ═════════════════════════════════════════════════════════════════════════
# 1. src/content.config.ts — добавляем коллекцию charter
# ═════════════════════════════════════════════════════════════════════════
FILES["src/content.config.ts"] = """\
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const music = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/music' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    language: z.enum(['ru', 'en']).default('ru'),
  }),
});

const charter = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/charter' }),
  schema: z.object({
    title: z.string(),
    number: z.string(),
    book: z.number(),
    bookTitle: z.string(),
    part: z.number(),
    partTitle: z.string(),
    order: z.number(),
    source: z.string().optional(),
  }),
});

export const collections = { music, charter };
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. src/components/CharterNav.astro — боковая навигация
# ═════════════════════════════════════════════════════════════════════════
FILES["src/components/CharterNav.astro"] = """\
---
interface NavArticle {
  number: string;
  title: string;
  part: number;
  partTitle: string;
  slug: string;   // '1-10'
  href: string;   // '/hartia/charter/kniga-1/1-10'
  isCurrent: boolean;
}

interface Props {
  book: number;
  bookTitle: string;
  bookHref: string;
  articles: NavArticle[];
}

const { book, bookTitle, bookHref, articles } = Astro.props;

// Сгруппировать по частям
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

<aside class="charter-nav">
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

<style>
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
    .charter-nav {
      position: static;
      max-height: none;
      border-right: none;
      border-bottom: 1px solid var(--gold-dim);
      padding: 1.5rem 0;
      margin-bottom: 2rem;
    }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 3. src/pages/charter/index.astro — оглавление Хартии
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/charter/index.astro"] = """\
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import '../../styles/global.css';

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const url = (path: string) => `${base}${path.startsWith('/') ? path : `/${path}`}`;

const articles = await getCollection('charter');

// Группируем по книгам
const byBook: Record<number, {
  bookTitle: string;
  count: number;
  parts: Set<number>;
}> = {};

for (const a of articles) {
  const n = a.data.book;
  if (!byBook[n]) {
    byBook[n] = { bookTitle: a.data.bookTitle, count: 0, parts: new Set() };
  }
  byBook[n].count += 1;
  byBook[n].parts.add(a.data.part);
}

const roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'];
const books = Object.keys(byBook)
  .map(Number)
  .sort((a, b) => a - b)
  .map((n) => ({
    num: n,
    roman: roman[n] || String(n),
    title: byBook[n].bookTitle,
    count: byBook[n].count,
    parts: byBook[n].parts.size,
  }));

const title = 'Хартия';
const description =
  'Сводный регламент Хартии 5.0 — Протокол Цивилизации Будущего. ' +
  'Восемь книг, 314 статей.';
---

<BaseLayout title={title} description={description}>
  <section class="charter-hero">
    <div class="container">
      <p class="charter-hero__label mono">Сводный регламент · Модульная версия</p>
      <h1 class="charter-hero__title">Хартия</h1>
      <p class="charter-hero__sub">
        Восемь книг. {articles.length} статей. Один протокол.
        Читается по частям — от преамбулы до экспериментальных
        протоколов Первой сотни.
      </p>
    </div>
  </section>

  <section class="books">
    <div class="container">
      <ul class="books__grid">
        {books.map((b) => (
          <li>
            <a href={url(`/charter/kniga-${b.num}`)} class="book-card">
              <span class="book-card__num mono">Книга {b.roman}</span>
              <h2 class="book-card__title">{b.title}</h2>
              <span class="book-card__meta">
                {b.count} статей · {b.parts} частей
              </span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  </section>
</BaseLayout>

<style>
  .charter-hero {
    padding-block: 5rem 4rem;
    text-align: center;
  }

  .charter-hero__label {
    color: var(--gold);
    margin-bottom: 1.5rem;
  }

  .charter-hero__title {
    font-size: clamp(2.5rem, 6vw, 4rem);
    margin-bottom: 1.5rem;
  }

  .charter-hero__sub {
    max-width: 56ch;
    margin-inline: auto;
    color: var(--text-secondary);
    font-size: 1.05rem;
    line-height: 1.7;
  }

  .books { padding-block: 2rem 5rem; }

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
  }

  .book-card:hover {
    border-color: var(--gold);
    background: var(--bg-subtle);
    transform: translateY(-2px);
  }

  .book-card__num {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: var(--gold);
    margin-bottom: 0.75rem;
  }

  .book-card__title {
    font-size: 1.35rem;
    margin-bottom: 1rem;
    line-height: 1.2;
    flex: 1;
    transition: color var(--transition);
  }

  .book-card:hover .book-card__title { color: var(--gold-bright); }

  .book-card__meta {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding-top: 1rem;
    border-top: 1px solid var(--gold-dim);
  }

  @media (max-width: 720px) {
    .books__grid { grid-template-columns: 1fr; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 4. src/pages/charter/[book]/index.astro — страница книги
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/charter/[book]/index.astro"] = """\
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';
import '../../../styles/global.css';

export async function getStaticPaths() {
  const all = await getCollection('charter');
  const bookNums = [...new Set(all.map((a) => a.data.book))];
  return bookNums.map((n) => ({
    params: { book: `kniga-${n}` },
    props: { bookNum: n, allArticles: all },
  }));
}

const { bookNum, allArticles } = Astro.props;
const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const url = (path: string) => `${base}${path.startsWith('/') ? path : `/${path}`}`;

const articles = allArticles
  .filter((a) => a.data.book === bookNum)
  .sort((a, b) => a.data.order - b.data.order);

const bookTitle = articles[0]?.data.bookTitle || '';

const roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'];

// Группировка по частям
const byPart: Record<number, { partTitle: string; items: typeof articles }> = {};
for (const a of articles) {
  const p = a.data.part;
  if (!byPart[p]) {
    byPart[p] = { partTitle: a.data.partTitle, items: [] };
  }
  byPart[p].items.push(a);
}
const parts = Object.keys(byPart).map(Number).sort((a, b) => a - b);

const title = `Книга ${roman[bookNum]} — ${bookTitle}`;
const description = `${bookTitle}: ${articles.length} статей в ${parts.length} частях. Хартия 5.0.`;
---

<BaseLayout title={title} description={description}>
  <section class="book-hero">
    <div class="container">
      <nav class="crumbs mono">
        <a href={url('/charter')}>Хартия</a>
        <span class="crumbs__sep">/</span>
        <span>Книга {roman[bookNum]}</span>
      </nav>

      <p class="book-hero__label mono">Книга {roman[bookNum]}</p>
      <h1 class="book-hero__title">{bookTitle}</h1>
      <p class="book-hero__meta">
        {articles.length} статей · {parts.length} частей
      </p>
    </div>
  </section>

  <section class="book-toc">
    <div class="container">
      {parts.map((p) => {
        const group = byPart[p];
        return (
          <section class="part">
            <header class="part__head">
              <span class="part__num mono">Часть {p}</span>
              <h2 class="part__title">{group.partTitle}</h2>
            </header>

            <ul class="part__list">
              {group.items.map((a) => {
                const slug = a.data.number.replace(/\\./g, '-');
                const href = url(`/charter/kniga-${bookNum}/${slug}`);
                return (
                  <li>
                    <a href={href} class="article-row">
                      <span class="article-row__num mono">{a.data.number}</span>
                      <span class="article-row__title">{a.data.title}</span>
                      <span class="article-row__arrow" aria-hidden="true">→</span>
                    </a>
                  </li>
                );
              })}
            </ul>
          </section>
        );
      })}
    </div>
  </section>
</BaseLayout>

<style>
  .book-hero {
    padding-block: 4rem 3rem;
    border-bottom: 1px solid var(--gold-dim);
  }

  .crumbs {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
  }

  .crumbs a { color: var(--text-secondary); }
  .crumbs a:hover { color: var(--gold-bright); }
  .crumbs__sep { margin-inline: 0.5rem; color: var(--gold-dim); }

  .book-hero__label {
    color: var(--gold);
    margin-bottom: 1rem;
  }

  .book-hero__title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    margin-bottom: 1rem;
    line-height: 1.1;
  }

  .book-hero__meta {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
  }

  .book-toc { padding-block: 4rem 5rem; }

  .part {
    margin-bottom: 3.5rem;
  }

  .part__head {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1.25rem;
    align-items: baseline;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--gold-dim);
  }

  .part__num {
    color: var(--gold);
    font-size: 0.75rem;
    letter-spacing: 0.15em;
  }

  .part__title {
    font-size: 1.35rem;
    font-weight: 500;
    line-height: 1.3;
  }

  .part__list {
    list-style: none;
    display: grid;
    gap: 0.25rem;
  }

  .article-row {
    display: grid;
    grid-template-columns: 4rem 1fr auto;
    gap: 1.25rem;
    align-items: baseline;
    padding: 0.85rem 1rem;
    border-left: 2px solid transparent;
    transition: all var(--transition);
    border-radius: 2px;
  }

  .article-row:hover {
    background: var(--bg-subtle);
    border-left-color: var(--gold);
    padding-left: 1.25rem;
  }

  .article-row__num {
    font-size: 0.75rem;
    color: var(--gold-dim);
    letter-spacing: 0.08em;
  }

  .article-row:hover .article-row__num { color: var(--gold); }

  .article-row__title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    color: var(--text-primary);
    line-height: 1.3;
  }

  .article-row:hover .article-row__title { color: var(--gold-bright); }

  .article-row__arrow {
    color: var(--gold-dim);
    transition: all var(--transition);
    opacity: 0;
  }

  .article-row:hover .article-row__arrow {
    color: var(--gold);
    opacity: 1;
    transform: translateX(4px);
  }

  @media (max-width: 640px) {
    .article-row {
      grid-template-columns: 3.5rem 1fr;
      gap: 0.75rem;
      padding: 0.75rem 0.5rem;
    }
    .article-row__arrow { display: none; }
    .article-row__title { font-size: 1rem; }
    .part__head { grid-template-columns: 1fr; gap: 0.5rem; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 5. src/pages/charter/[book]/[article].astro — статья
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/charter/[book]/[article].astro"] = """\
---
import { getCollection, render } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';
import CharterNav from '../../../components/CharterNav.astro';
import '../../../styles/global.css';

export async function getStaticPaths() {
  const all = await getCollection('charter');
  return all.map((a) => ({
    params: {
      book: `kniga-${a.data.book}`,
      article: a.data.number.replace(/\\./g, '-'),
    },
    props: { article: a, allArticles: all },
  }));
}

const { article, allArticles } = Astro.props;
const { Content } = await render(article);

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const url = (path: string) => `${base}${path.startsWith('/') ? path : `/${path}`}`;

const bookNum = article.data.book;
const bookTitle = article.data.bookTitle;
const roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'];

// Все статьи книги — для боковой навигации
const bookArticles = allArticles
  .filter((a) => a.data.book === bookNum)
  .sort((a, b) => a.data.order - b.data.order);

const navArticles = bookArticles.map((a) => {
  const slug = a.data.number.replace(/\\./g, '-');
  return {
    number: a.data.number,
    title: a.data.title,
    part: a.data.part,
    partTitle: a.data.partTitle,
    slug,
    href: url(`/charter/kniga-${bookNum}/${slug}`),
    isCurrent: a.data.number === article.data.number,
  };
});

// Соседние статьи для навигации внизу
const idx = bookArticles.findIndex((a) => a.data.number === article.data.number);
const prev = idx > 0 ? bookArticles[idx - 1] : null;
const next = idx < bookArticles.length - 1 ? bookArticles[idx + 1] : null;

function slugOf(a: typeof article) {
  return a.data.number.replace(/\\./g, '-');
}

const title = `Статья ${article.data.number}. ${article.data.title}`;
const description = `${article.data.title} — Хартия 5.0, Книга ${roman[bookNum]}, Часть ${article.data.part}.`;
---

<BaseLayout title={title} description={description}>
  <div class="charter-layout container">
    <CharterNav
      book={bookNum}
      bookTitle={bookTitle}
      bookHref={url(`/charter/kniga-${bookNum}`)}
      articles={navArticles}
    />

    <main class="charter-main">
      <nav class="crumbs mono">
        <a href={url('/charter')}>Хартия</a>
        <span class="crumbs__sep">/</span>
        <a href={url(`/charter/kniga-${bookNum}`)}>Книга {roman[bookNum]}</a>
        <span class="crumbs__sep">/</span>
        <span>Статья {article.data.number}</span>
      </nav>

      <header class="article-head">
        <p class="article-head__meta mono">
          <span>Часть {article.data.part}</span>
          <span class="article-head__meta-sep">·</span>
          <span>{article.data.partTitle}</span>
        </p>

        <h1 class="article-head__title">
          <span class="article-head__num mono">{article.data.number}.</span>
          {article.data.title}
        </h1>

        {article.data.source && (
          <p class="article-head__source mono">({article.data.source})</p>
        )}
      </header>

      <article class="article-body">
        <Content />
      </article>

      {(prev || next) && (
        <nav class="article-pager">
          {prev ? (
            <a
              href={url(`/charter/kniga-${bookNum}/${slugOf(prev)}`)}
              class="article-pager__item article-pager__item--prev"
            >
              <span class="article-pager__label mono">← Предыдущая</span>
              <span class="article-pager__title">
                {prev.data.number}. {prev.data.title}
              </span>
            </a>
          ) : <span />}

          {next ? (
            <a
              href={url(`/charter/kniga-${bookNum}/${slugOf(next)}`)}
              class="article-pager__item article-pager__item--next"
            >
              <span class="article-pager__label mono">Следующая →</span>
              <span class="article-pager__title">
                {next.data.number}. {next.data.title}
              </span>
            </a>
          ) : <span />}
        </nav>
      )}
    </main>
  </div>
</BaseLayout>

<style>
  .charter-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 3rem;
    padding-block: 3rem 5rem;
    align-items: start;
  }

  .charter-main { min-width: 0; }

  .crumbs {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
  }

  .crumbs a { color: var(--text-secondary); }
  .crumbs a:hover { color: var(--gold-bright); }
  .crumbs__sep { margin-inline: 0.5rem; color: var(--gold-dim); }

  .article-head {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--gold-dim);
  }

  .article-head__meta {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    margin-bottom: 1rem;
    text-transform: uppercase;
  }

  .article-head__meta-sep {
    margin-inline: 0.5rem;
    color: var(--gold-dim);
  }

  .article-head__title {
    font-size: clamp(1.75rem, 4vw, 2.75rem);
    line-height: 1.15;
    margin-bottom: 0.75rem;
  }

  .article-head__num {
    color: var(--gold);
    margin-right: 0.35rem;
  }

  .article-head__source {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    color: var(--text-muted);
  }

  .article-body {
    font-family: var(--font-body);
    font-size: 1.05rem;
    line-height: 1.75;
    color: var(--text-primary);
    white-space: pre-line;
  }

  .article-body :global(p) { margin-bottom: 1em; }

  .article-body :global(strong) {
    color: var(--gold-bright);
    font-weight: 500;
  }

  .article-pager {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 5rem;
    padding-top: 2rem;
    border-top: 1px solid var(--gold-dim);
  }

  .article-pager__item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem 1.25rem;
    border: 1px solid var(--gold-dim);
    transition: all var(--transition);
    min-height: 5rem;
  }

  .article-pager__item:hover {
    border-color: var(--gold);
    background: var(--bg-subtle);
  }

  .article-pager__item--next { text-align: right; }

  .article-pager__label {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--gold);
    text-transform: uppercase;
  }

  .article-pager__title {
    font-family: var(--font-display);
    font-size: 1.05rem;
    color: var(--text-primary);
    line-height: 1.3;
  }

  @media (max-width: 960px) {
    .charter-layout {
      grid-template-columns: 1fr;
      gap: 0;
      padding-block: 2rem 3rem;
    }
  }

  @media (max-width: 640px) {
    .article-pager { grid-template-columns: 1fr; }
    .article-pager__item--next { text-align: left; }
  }
</style>
"""


def apply() -> tuple[int, int]:
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


def main() -> int:
    if not ROOT.exists():
        print(f"[ERR] нет {ROOT}")
        return 1

    print(f"Проект: {ROOT}")
    if DRY_RUN: print("Режим: --dry-run")
    if FORCE: print("Режим: --force")
    print()

    print("── Файлы ──")
    w, s = apply()

    print()
    print(f"Записано: {w}, пропущено: {s}.")
    print()
    print("Дальше:")
    print("  npm run dev")
    print("  Открыть:")
    print("    http://localhost:4321/hartia/charter")
    print("    http://localhost:4321/hartia/charter/kniga-1")
    print("    http://localhost:4321/hartia/charter/kniga-1/1-10")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())