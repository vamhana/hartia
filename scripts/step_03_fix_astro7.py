#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Фикс Шага 3 для Astro 7.

Astro 7 изменил API Content Collections:
  - config.ts → content.config.ts
  - обязательный loader
  - getCollection().render() → render(entry)
  - YAML не парсится нативно

Запуск:
    python scripts/step_03_fix_astro7.py --dry-run
    python scripts/step_03_fix_astro7.py
    python scripts/step_03_fix_astro7.py --force
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

RELEASE_BASE = "https://github.com/vamhana/hartia/releases/download/audio-v1"

FILES: dict[str, str] = {}
DELETE: list[str] = [
    "src/content/config.ts",   # старый путь
    "src/data/tracks.yaml",    # заменяется на tracks.ts
]

# ═════════════════════════════════════════════════════════════════════════
# 1. src/content.config.ts — новый формат Astro 7
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

export const collections = { music };
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. src/data/tracks.ts — вместо yaml
# ═════════════════════════════════════════════════════════════════════════
FILES["src/data/tracks.ts"] = f"""\
export interface Track {{
  slug: string;
  title: string;
  file: string;
  duration: string;
  year: number;
  cover: string;
  tags: string[];
  description: string;
}}

export const release_base = '{RELEASE_BASE}';

export const tracks: Track[] = [
  {{
    slug: 'komfortnyj-ad',
    title: 'Комфортный ад',
    file: 'komfortnyj-ad.mp3',
    duration: '4:20',
    year: 2026,
    cover: '/covers/komfortnyj-ad.jpg',
    tags: ['phonk', 'hyperpop', 'anti-consumerism'],
    description: 'Пробуждение от сна системы. Манифест тех, кто устал быть расходным материалом.',
  }},
  {{
    slug: 'upgrade-pustoty',
    title: 'Апгрейд пустоты',
    file: 'upgrade-pustoty.mp3',
    duration: '4:55',
    year: 2026,
    cover: '/covers/upgrade-pustoty.png',
    tags: ['phonk', 'industrial', 'transformation'],
    description: 'После взрыва не строю стены. Взрыв — это диагноз. О сборке себя из пепла.',
  }},
  {{
    slug: 'paketik-dlya-spyashchih',
    title: 'Пакетик для спящих',
    file: 'paketik-dlya-spyashchih.mp3',
    duration: '3:48',
    year: 2026,
    cover: '/covers/paketik-dlya-spyashchih.jpg',
    tags: ['phonk', 'satire', 'awakening'],
    description: 'О тех, кто заваривает собственный сон. Одуванчик против пакетика.',
  }},
  {{
    slug: 'na-u-yu',
    title: 'На-у-ю',
    file: 'na-u-yu.mp3',
    duration: '3:15',
    year: 2026,
    cover: '/covers/na-u-yu.jpg',
    tags: ['phonk', 'banks', 'freedom'],
    description: 'Все банки в ряд намотаю. Прощание с долговой системой.',
  }},
  {{
    slug: 'na-u-yu-wrapped',
    title: 'Na-U-Yu Wrapped',
    file: 'na-u-yu-wrapped.mp3',
    duration: '3:15',
    year: 2026,
    cover: '/covers/na-u-yu-wrapped.jpg',
    tags: ['phonk', 'banks', 'english'],
    description: 'English version. All the banks in a row I\\'ll wrap.',
  }},
];

export default {{ release_base, tracks }};
"""

# ═════════════════════════════════════════════════════════════════════════
# 3. src/pages/music.astro — обновлённый импорт + удалена лишняя типизация
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/music.astro"] = """\
---
import BaseLayout from '../layouts/BaseLayout.astro';
import MusicPlayer from '../components/MusicPlayer.astro';
import TrackCard from '../components/TrackCard.astro';
import '../styles/global.css';

import { tracks, release_base } from '../data/tracks';

const title = 'Музыка Хартии';
const description =
  'Пять треков агрессивного фонка — спутники текста Хартии. ' +
  'Слушайте, читайте тексты, скачивайте свободно.';
---

<BaseLayout title={title} description={description}>
  <section class="music-hero">
    <div class="container">
      <p class="music-hero__label mono">Музыка · 2026 · 5 треков</p>
      <h1 class="music-hero__title">Музыка Хартии</h1>
      <p class="music-hero__sub">
        Пять треков, написанных как спутники текста.
        Слушайте. Читайте тексты. Скачивайте свободно.
        Музыка — не фон для чтения, а отдельный голос того же протеста.
      </p>
    </div>
  </section>

  <section class="music-player">
    <div class="container">
      <MusicPlayer tracks={tracks} releaseBase={release_base} />
    </div>
  </section>

  <section class="music-list">
    <div class="container">
      <header class="section-head">
        <span class="section-head__num mono">V</span>
        <h2 class="section-head__title">Треки</h2>
        <p class="section-head__sub">Каждый — со своей страницей и текстом.</p>
      </header>

      <ul class="music-list__grid">
        {tracks.map((t) => (
          <li>
            <TrackCard
              slug={t.slug}
              title={t.title}
              cover={t.cover}
              description={t.description}
              duration={t.duration}
              releaseBase={release_base}
              file={t.file}
            />
          </li>
        ))}
      </ul>
    </div>
  </section>

  <section class="music-foot">
    <div class="container prose">
      <p>
        Все треки распространяются свободно по лицензии{' '}
        <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">
          CC BY-SA 4.0
        </a>. Скачивайте, делитесь, используйте. Хартия — открытый код,
        и музыка — тоже.
      </p>
    </div>
  </section>
</BaseLayout>

<style>
  .music-hero {
    padding-block: 5rem 3rem;
    text-align: center;
  }

  .music-hero__label {
    margin-bottom: 1.5rem;
    color: var(--cyan);
  }

  .music-hero__title {
    font-size: clamp(2.5rem, 6vw, 4rem);
    margin-bottom: 1.5rem;
  }

  .music-hero__sub {
    max-width: 54ch;
    margin-inline: auto;
    color: var(--text-secondary);
    font-size: 1.05rem;
    line-height: 1.7;
  }

  .music-player { padding-block: 2rem 5rem; }

  .music-list { padding-block: 3rem 5rem; }

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
  }

  .section-head__title { margin: 0; font-size: clamp(1.75rem, 3vw, 2.5rem); }

  .section-head__sub {
    font-style: italic;
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin: 0;
  }

  .music-list__grid {
    list-style: none;
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .music-foot {
    padding-block: 4rem;
    margin-top: 3rem;
    border-top: 1px solid var(--gold-dim);
    text-align: center;
  }

  .music-foot p { color: var(--text-secondary); }

  @media (max-width: 720px) {
    .section-head { grid-template-columns: 1fr; }
    .section-head__num { grid-row: auto; padding-top: 0; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 4. src/pages/music/[slug].astro — новый render() + getEntry
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/music/[slug].astro"] = """\
---
import { getCollection, render } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import MusicPlayer from '../../components/MusicPlayer.astro';
import '../../styles/global.css';

import { tracks, release_base } from '../../data/tracks';

export async function getStaticPaths() {
  return tracks.map((t) => ({
    params: { slug: t.slug },
    props: { track: t, allTracks: tracks },
  }));
}

const { track, allTracks } = Astro.props;

const lyrics = await getCollection('music');
const lyricsEntry = lyrics.find((e) => e.id === track.slug);

let Content = null;
if (lyricsEntry) {
  const rendered = await render(lyricsEntry);
  Content = rendered.Content;
}

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const coverUrl = `${base}${track.cover}`;
const downloadUrl = `${release_base}/${track.file}`;

const others = allTracks.filter((t) => t.slug !== track.slug);

const pageTitle = `${track.title} — текст и скачать`;
const pageDesc = track.description;
---

<BaseLayout title={pageTitle} description={pageDesc}>
  <section class="track">
    <div class="container">
      <nav class="track__crumbs mono">
        <a href={`${base}/music`}>Музыка</a>
        <span class="track__crumbs-sep">/</span>
        <span>{track.title}</span>
      </nav>

      <header class="track__head">
        <div class="track__cover">
          <img src={coverUrl} alt={track.title} />
        </div>

        <div class="track__meta">
          <p class="track__label mono">{track.year} · {track.duration}</p>
          <h1 class="track__title">{track.title}</h1>
          <p class="track__desc">{track.description}</p>

          <div class="track__tags">
            {track.tags.map((tag) => (
              <span class="track__tag mono">{tag}</span>
            ))}
          </div>

          <div class="track__actions">
            <a href={downloadUrl} class="btn btn--primary" download data-download={track.slug}>
              ↓ Скачать MP3
            </a>
            <a href={`${base}/music`} class="btn">← Все треки</a>
          </div>
        </div>
      </header>
    </div>
  </section>

  <section class="track__player">
    <div class="container">
      <MusicPlayer tracks={[track]} releaseBase={release_base} />
    </div>
  </section>

  {Content && (
    <section class="track__lyrics">
      <div class="container prose">
        <h2 class="track__lyrics-title">Текст</h2>
        <div class="track__lyrics-body">
          <Content />
        </div>
      </div>
    </section>
  )}

  <section class="track__others">
    <div class="container">
      <h2 class="track__others-title">Другие треки</h2>
      <ul class="track__others-list">
        {others.map((t) => (
          <li>
            <a href={`${base}/music/${t.slug}`} class="track__other">
              <span class="track__other-title">{t.title}</span>
              <span class="track__other-dur mono">{t.duration}</span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  </section>
</BaseLayout>

<style>
  .track { padding-block: 3rem 2rem; }

  .track__crumbs {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
  }

  .track__crumbs a { color: var(--text-secondary); }
  .track__crumbs a:hover { color: var(--gold-bright); }
  .track__crumbs-sep { margin-inline: 0.5rem; color: var(--gold-dim); }

  .track__head {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 3rem;
    align-items: start;
  }

  .track__cover {
    aspect-ratio: 1;
    border: 1px solid var(--gold-dim);
    background: var(--bg-subtle);
    overflow: hidden;
  }

  .track__cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .track__label { color: var(--cyan); margin-bottom: 1rem; }

  .track__title {
    font-size: clamp(2rem, 4vw, 3rem);
    margin-bottom: 1rem;
    line-height: 1.1;
  }

  .track__desc {
    color: var(--text-secondary);
    font-size: 1.05rem;
    line-height: 1.65;
    margin-bottom: 1.5rem;
  }

  .track__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 2rem;
  }

  .track__tag {
    font-size: 0.65rem;
    color: var(--gold);
    border: 1px solid var(--gold-dim);
    padding: 0.3rem 0.7rem;
    letter-spacing: 0.15em;
  }

  .track__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .track__player { padding-block: 2rem 4rem; }

  .track__lyrics {
    padding-block: 3rem 5rem;
    border-top: 1px solid var(--gold-dim);
  }

  .track__lyrics-title {
    text-align: center;
    margin-bottom: 3rem;
    font-size: 1.5rem;
    font-family: var(--font-mono);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    font-weight: 400;
  }

  .track__lyrics-body {
    font-family: var(--font-body);
    font-size: 1.05rem;
    line-height: 1.85;
    color: var(--text-primary);
  }

  .track__lyrics-body :global(p) { margin-bottom: 1.25em; }
  .track__lyrics-body :global(strong) {
    color: var(--gold-bright);
    font-weight: 500;
    font-style: normal;
    display: block;
    margin-top: 1.5em;
    margin-bottom: 0.75em;
    font-family: var(--font-mono);
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
  }
  .track__lyrics-body :global(em) { color: var(--text-secondary); }

  .track__others {
    padding-block: 3rem 5rem;
    border-top: 1px solid var(--gold-dim);
  }

  .track__others-title {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    color: var(--gold);
    font-family: var(--font-mono);
    font-weight: 400;
    letter-spacing: 0.15em;
    text-transform: uppercase;
  }

  .track__others-list { list-style: none; }

  .track__other {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid var(--gold-dim);
    transition: all var(--transition);
  }

  .track__other:hover {
    padding-left: 0.5rem;
    color: var(--gold-bright);
  }

  .track__other-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
  }

  .track__other-dur {
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  @media (max-width: 720px) {
    .track__head { grid-template-columns: 1fr; gap: 1.5rem; }
    .track__cover { max-width: 260px; }
  }
</style>
"""


def apply() -> tuple[int, int, int]:
    written = skipped = deleted = 0

    # Удаление
    for rel in DELETE:
        full = ROOT / rel
        if full.exists():
            if DRY_RUN:
                print(f"[del?]  {rel}")
            else:
                full.unlink()
                print(f"[del]   {rel}")
                deleted += 1

    # Запись
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

    return written, skipped, deleted


def main() -> int:
    if not ROOT.exists():
        print(f"[ERR] нет {ROOT}")
        return 1

    print(f"Проект: {ROOT}")
    if DRY_RUN: print("Режим: --dry-run")
    if FORCE: print("Режим: --force")
    print()

    print("── Файлы ──")
    w, s, d = apply()

    print()
    print(f"Записано: {w}, пропущено: {s}, удалено: {d}.")
    print()
    print("Дальше:")
    print("  npm run dev")
    print("  Открыть http://localhost:4321/hartia/music")
    print()
    print("  git add .")
    print('  git commit -m "Fix content collections for Astro 7"')
    print("  git push")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())