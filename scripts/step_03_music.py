#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Шаг 3: страница /music + плеер + страницы треков.

Создаёт:
  - src/data/tracks.yaml           — метаданные 5 треков
  - src/content/config.ts          — коллекция music (если ещё нет)
  - src/content/music/*.md         — 5 страниц с текстами
  - src/components/MusicPlayer.astro
  - src/components/TrackCard.astro
  - src/pages/music.astro
  - src/pages/music/[slug].astro
  - public/covers/_placeholder.svg — заглушка обложки
  - public/audio/README.md         — инструкция

Запуск:
    python scripts/step_03_music.py --dry-run
    python scripts/step_03_music.py
    python scripts/step_03_music.py --force
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

# Релиз на GitHub — пользователь создаст его вручную
RELEASE_BASE = "https://github.com/vamhana/hartia/releases/download/audio-v1"

FILES: dict[str, str] = {}

# ═════════════════════════════════════════════════════════════════════════
# 1. src/data/tracks.yaml
# ═════════════════════════════════════════════════════════════════════════
FILES["src/data/tracks.yaml"] = f"""\
# Метаданные треков. Обновляй вручную после создания релиза.
# Файлы лежат в GitHub Releases: {RELEASE_BASE}
# Обложки — в public/covers/ (извлекаются скриптом extract_covers.py)

release_base: "{RELEASE_BASE}"

tracks:
  - slug: komfortnyj-ad
    title: Комфортный ад
    file: komfortnyj-ad.mp3
    duration: "4:20"
    year: 2026
    cover: /covers/komfortnyj-ad.jpg
    tags: [phonk, hyperpop, anti-consumerism]
    description: Пробуждение от сна системы. Манифест тех, кто устал быть расходным материалом.

  - slug: upgrade-pustoty
    title: Апгрейд пустоты
    file: upgrade-pustoty.mp3
    duration: "4:55"
    year: 2026
    cover: /covers/upgrade-pustoty.jpg
    tags: [phonk, industrial, transformation]
    description: После взрыва не строю стены. Взрыв — это диагноз. О сборке себя из пепла.

  - slug: paketik-dlya-spyashchih
    title: Пакетик для спящих
    file: paketik-dlya-spyashchih.mp3
    duration: "3:48"
    year: 2026
    cover: /covers/paketik-dlya-spyashchih.jpg
    tags: [phonk, satire, awakening]
    description: О тех, кто заваривает собственный сон. Одуванчик против пакетика.

  - slug: na-u-yu
    title: На-у-ю
    file: na-u-yu.mp3
    duration: "3:15"
    year: 2026
    cover: /covers/na-u-yu.jpg
    tags: [phonk, banks, freedom]
    description: Все банки в ряд намотаю. Прощание с долговой системой.

  - slug: na-u-yu-wrapped
    title: Na-U-Yu Wrapped
    file: na-u-yu-wrapped.mp3
    duration: "3:15"
    year: 2026
    cover: /covers/na-u-yu-wrapped.jpg
    tags: [phonk, banks, english]
    description: English version. All the banks in a row I'll wrap.
"""

# ═════════════════════════════════════════════════════════════════════════
# 2. src/content/config.ts
# ═════════════════════════════════════════════════════════════════════════
FILES["src/content/config.ts"] = """\
import { defineCollection, z } from 'astro:content';

const music = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    lyrics_en: z.string().optional(),
    language: z.enum(['ru', 'en']).default('ru'),
  }),
});

export const collections = { music };
"""

# ═════════════════════════════════════════════════════════════════════════
# 3. src/content/music/*.md — тексты (пользователь дополнит)
# ═════════════════════════════════════════════════════════════════════════
FILES["src/content/music/komfortnyj-ad.md"] = """\
---
title: Комфортный ад
slug: komfortnyj-ad
language: ru
---

**(Куплет 1: Завод душ)**

Конвейер мечтает за нас, штампуя типовой успех.
Мы — расходный материал на заводе спешащих душ.
Нас считают по головам, но не слышат наши души.
Выходной — чтоб зарядить аккумулятор на уютной муке.

**(Припев 1)**

На краю... их удобного мира...
И ЭТО НАШ КОМФОРТНЫЙ АД!
Где счастье — это рай с кодом доступа.
Мой сигнал «ОТМЕНА» не входит в их расчёт!
Поэтому эту клетку тепла — разорву изнутри!
Не прошу, не молю — я уже сорвал предохрани!
СИСТЕМА, ОТБОЙ!

**(Куплет 2: Система «Человек»)**

Загрузили в нас клише, обновили до версии «Покорный».
Система «Человек» работает, ошибка «Воля» — неисправность.
Они следят, чтобы шёл ровно тот, кто встроен в алгоритм.
Я удаляю себя из их списка живых, но спящих.

**(Припев 2)**

На краю... их удобного мира...
И ЭТО НАШ КОМФОРТНЫЙ АД!
...

**(Бридж: Сон наяву)**

А когда выключают свет, и экран не светит в лицо,
Я чувствую, как сон наяву трещит по швам, как лёд.
Кто я, когда не сплю? Чей во мне говорит голос?
Не их, не их! Он тише их, но это — МОЙ ЗОВ.

**(Финальный прорыв)**

Я... ЛОМАЮ КОД ДОСТУПА К ЭТОМУ РАЮ-АДУ!
Я... СХОЖУ С КОНВЕЙЕРА НА ЗАВОДЕ ДУШ!
Я... ВЫКЛЮЧАЮ СИСТЕМУ «ЧЕЛОВЕК»!
Я... ПРОБУЖДАЮСЬ ОТ ЭТОГО СНА!

МОЙ КОМФОРТ — ЭТО БЫТЬ ЖИВЫМ. МОЙ АД — ЭТО БЫТЬ РАБОМ. ВЫБОР СДЕЛАН.
"""

FILES["src/content/music/upgrade-pustoty.md"] = """\
---
title: Апгрейд пустоты
slug: upgrade-pustoty
language: ru
---

**Куплет 1**

После взрыва не строю стены. Взрыв — это диагноз.
Под ногами не плиты — пыль. Пыль моих решённых вопросов.
Их «надо» стали пеплом, их «должен» — пустотой.
Я стою не на руинах. Я стою на своей земле.
Впервые. Тихо.
И эта тишина гудит сильнее их рёва.
Это не конец. Это — сырьё.

**Припев**

И Я АПГРЕЙДИРУЮ ЭТУ ПУСТОТУ!
Из пепла «нет» и пыли «хватит»!
Я загружаю новое ядро — ЯДРО ТИШИНЫ!
Я — не архитектор! Я — САПЁР В СОБСТВЕННОЙ ДУШЕ!
Где каждый проводок страха я паяю на НЕЗАВИСИМОСТЬ!
Где каждый чип стыда — выжигаю паяльником правды!
АПГРЕЙД ИДЁТ! СИСТЕМА, Я ТВОЙ АНТИВИРУС!
Я — ТВОЁ ОБНУЛЕНИЕ!

*(полный текст — дополните при необходимости)*
"""

FILES["src/content/music/paketik-dlya-spyashchih.md"] = """\
---
title: Пакетик для спящих
slug: paketik-dlya-spyashchih
language: ru
---

**Куплет 1**

Они заваривают пакет, но заваривают туман —
Вода темнеет, но это не чай, это обман.
Бумага мокнет, превращаясь в распад,
Отбелена хлоркой — и в кружку, и рад, что это не яд.
А на дне, как всегда, — ничего, кроме ненужных затрат.
Они платят за то, чтоб заварить себе сон,
Потому что проснуться — это уже не их сезон.
Они пьют эту пыль, называя «уютом»,
А на дне — целлюлоза с прогорклым маршрутом.

**Припев**

А за забором — корни одуванчика!
Сушёный, молотый — он взбодрит без обманщика.
Эффект как от кофе, но без рабской цепи:
Сам собрал — сам заварил — сам проснулся — иди!
А они: пакетик в кружку, жидкость в живот.
А потом — «Помогите Алёшеньке!»,
Задают вопрос: «Почему так?» —
Потому что ты пил не корень, а клей и хлорку, дурак.
А ты пей одуванчик — и всё будет ништяк.
Их «рай» с кодом доступа — это их же — мрак.

*(полный текст — дополните при необходимости)*
"""

FILES["src/content/music/na-u-yu.md"] = """\
---
title: На-у-ю
slug: na-u-yu
language: ru
---

**[Intro — шёпот под бит]**

Так... По списку...
Кто тут у нас?

**[Verse 1]**

На-у-ю намотан Тинькофф, (Ха!)
На-у-ю намотан Сбер-банк, (Эй!)
Что тут у нас еще? А, ВТБ?
Ок, давай — очередной говно-банк!

**[Chorus — скандирование]**

На-у-ю, на-у-ю,
Все банки в ряд намотаю.
Баланс прёт, кредит молчит,
Я свободен — путь открыт!

**[Verse 2]**

Альфа-банк летит туда же,
На мотало, без подсказки!
Газпром-банк? Иди сюда!
Знай свое место, ты не в сказке!
Всех на уй, всех подряд,
Чистый кэшбек, я деньгам брат!

**[Bridge — речитатив]**

Сбер, ВТБ, Альфа, Тинькофф,
Все намотаны, без шансов.
Кто не спрятался — я не виноват,
Мой баланс теперь мой солдат.
А кто намотан — тому одна дорога:
Работать ртом у моего порога.

**[Chorus — повтор с усилением]**

На-у-ю, на-у-ю,
Все банки в ряд намотаю.
Баланс прёт, кредит молчит,
Я свободен — путь открыт!

**[Outro — затухание]**

Намотал... Намотал...
И пошел искать новый банк...
На-у-ю...
"""

FILES["src/content/music/na-u-yu-wrapped.md"] = """\
---
title: Na-U-Yu Wrapped
slug: na-u-yu-wrapped
language: en
---

**[Intro — whisper over beat]**

So... Down the list...
Who do we have here?

**[Verse 1]**

Na-u-yu wrapped Tinkoff, (Ha!)
Na-u-yu wrapped Sberbank, (Hey!)
What else we got? Ah, VTB?
Okay, come on — another shit bank!

**[Chorus — chanting]**

Na-u-yu, na-u-yu,
All the banks in a row I'll wrap.
Balance grows, credit shuts up,
I'm free — the path is open!

**[Verse 2]**

Alfa-Bank flies there too,
On the wrapper, no hints needed!
Gazprombank? Come here!
Know your place, you're not in a fairy tale!
All to hell, all in a row,
Clean cashback, I'm money's bro!

**[Bridge — spoken]**

Sber, VTB, Alfa, Tinkoff,
All wrapped up, no chance.
Who didn't hide — I'm not guilty,
My balance is now my soldier.
And who's wrapped — one road for him:
To work his mouth at my doorstep.

**[Chorus — repeat with intensity]**

Na-u-yu, na-u-yu,
All the banks in a row I'll wrap.
Balance grows, credit shuts up,
I'm free — the path is open!

**[Outro — fading]**

Wrapped... Wrapped...
And went to find a new bank...
Na-u-yu...
"""

# ═════════════════════════════════════════════════════════════════════════
# 4. src/components/MusicPlayer.astro
# ═════════════════════════════════════════════════════════════════════════
FILES["src/components/MusicPlayer.astro"] = """\
---
// Глобальный плеер. Живёт только на странице /music.
// Принимает массив треков: { slug, title, file, cover, duration }
interface Track {
  slug: string;
  title: string;
  file: string;
  cover: string;
  duration: string;
}

interface Props {
  tracks: Track[];
  releaseBase: string;
}

const { tracks, releaseBase } = Astro.props;
const audioBase = import.meta.env.BASE_URL.replace(/\\/$/, '');

const trackList = tracks.map((t) => ({
  ...t,
  src: `${releaseBase}/${t.file}`,
  href: `${audioBase}/music/${t.slug}`,
  cover: `${audioBase}${t.cover}`,
}));

const trackJson = JSON.stringify(trackList);
---

<div class="player" data-player>
  <div class="player__now">
    <div class="player__cover">
      <img
        src={trackList[0].cover}
        alt=""
        data-player-cover
        onerror={`this.style.display='none'`}
      />
    </div>

    <div class="player__info">
      <p class="player__label">Сейчас играет</p>
      <p class="player__title" data-player-title>{trackList[0].title}</p>
      <p class="player__time">
        <span data-player-current>0:00</span>
        <span class="player__time-sep">/</span>
        <span data-player-duration>{trackList[0].duration}</span>
      </p>
    </div>
  </div>

  <div class="player__progress">
    <input
      type="range"
      min="0"
      max="100"
      value="0"
      step="0.1"
      data-player-progress
      aria-label="Позиция"
    />
  </div>

  <div class="player__controls">
    <button
      type="button"
      class="player__btn"
      data-player-prev
      aria-label="Предыдущий"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
        <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
      </svg>
    </button>

    <button
      type="button"
      class="player__btn player__btn--play"
      data-player-toggle
      aria-label="Играть"
    >
      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" data-icon-play>
        <path d="M8 5v14l11-7z"/>
      </svg>
      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" data-icon-pause style="display:none">
        <path d="M6 5h4v14H6zm8 0h4v14h-4z"/>
      </svg>
    </button>

    <button
      type="button"
      class="player__btn"
      data-player-next
      aria-label="Следующий"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
        <path d="M16 6h2v12h-2zM6 18l8.5-6L6 6z"/>
      </svg>
    </button>

    <div class="player__volume">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
        <path d="M3 10v4h4l5 5V5L7 10H3zm13.5 2c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>
      </svg>
      <input
        type="range"
        min="0"
        max="100"
        value="80"
        step="1"
        data-player-volume
        aria-label="Громкость"
      />
    </div>
  </div>

  <audio
    preload="metadata"
    data-player-audio
    data-tracks={trackJson}
  ></audio>

  <ol class="player__playlist">
    {trackList.map((t, i) => (
      <li>
        <button
          type="button"
          class="player__track"
          data-player-track
          data-index={i}
        >
          <span class="player__track-num">{String(i + 1).padStart(2, '0')}</span>
          <span class="player__track-title">{t.title}</span>
          <span class="player__track-dur">{t.duration}</span>
        </button>
      </li>
    ))}
  </ol>
</div>

<script>
  interface TrackData {
    slug: string;
    title: string;
    src: string;
    cover: string;
    duration: string;
    href: string;
  }

  const root = document.querySelector('[data-player]') as HTMLElement | null;
  if (root) {
    const audio = root.querySelector('[data-player-audio]') as HTMLAudioElement;
    const tracks: TrackData[] = JSON.parse(audio.dataset.tracks || '[]');

    const elTitle = root.querySelector('[data-player-title]') as HTMLElement;
    const elCover = root.querySelector('[data-player-cover]') as HTMLImageElement;
    const elCurrent = root.querySelector('[data-player-current]') as HTMLElement;
    const elDuration = root.querySelector('[data-player-duration]') as HTMLElement;
    const elProgress = root.querySelector('[data-player-progress]') as HTMLInputElement;
    const elVolume = root.querySelector('[data-player-volume]') as HTMLInputElement;
    const btnToggle = root.querySelector('[data-player-toggle]') as HTMLButtonElement;
    const btnPrev = root.querySelector('[data-player-prev]') as HTMLButtonElement;
    const btnNext = root.querySelector('[data-player-next]') as HTMLButtonElement;
    const iconPlay = root.querySelector('[data-icon-play]') as SVGElement;
    const iconPause = root.querySelector('[data-icon-pause]') as SVGElement;
    const trackBtns = root.querySelectorAll('[data-player-track]');

    let current = 0;

    function fmt(sec: number): string {
      if (!isFinite(sec)) return '0:00';
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${m}:${String(s).padStart(2, '0')}`;
    }

    function load(i: number) {
      current = i;
      const t = tracks[i];
      audio.src = t.src;
      elTitle.textContent = t.title;
      elDuration.textContent = t.duration || '0:00';
      if (t.cover) {
        elCover.src = t.cover;
        elCover.style.display = '';
      } else {
        elCover.style.display = 'none';
      }
      trackBtns.forEach((btn, idx) => {
        (btn as HTMLElement).classList.toggle('is-active', idx === i);
      });
    }

    function play() {
      audio.play().then(() => {
        iconPlay.style.display = 'none';
        iconPause.style.display = '';
      }).catch(() => {});
    }

    function pause() {
      audio.pause();
      iconPlay.style.display = '';
      iconPause.style.display = 'none';
    }

    btnToggle.addEventListener('click', () => {
      if (audio.paused) play();
      else pause();
    });

    btnNext.addEventListener('click', () => {
      load((current + 1) % tracks.length);
      play();
    });

    btnPrev.addEventListener('click', () => {
      load((current - 1 + tracks.length) % tracks.length);
      play();
    });

    trackBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const i = Number((btn as HTMLElement).dataset.index);
        if (i === current && !audio.paused) {
          pause();
          return;
        }
        load(i);
        play();
      });
    });

    audio.addEventListener('timeupdate', () => {
      if (audio.duration) {
        elProgress.value = String((audio.currentTime / audio.duration) * 100);
        elCurrent.textContent = fmt(audio.currentTime);
      }
    });

    audio.addEventListener('loadedmetadata', () => {
      elDuration.textContent = fmt(audio.duration);
    });

    audio.addEventListener('ended', () => {
      load((current + 1) % tracks.length);
      play();
    });

    elProgress.addEventListener('input', () => {
      if (audio.duration) {
        audio.currentTime = (Number(elProgress.value) / 100) * audio.duration;
      }
    });

    elVolume.addEventListener('input', () => {
      audio.volume = Number(elVolume.value) / 100;
    });
    audio.volume = Number(elVolume.value) / 100;

    load(0);
  }
</script>

<style>
  .player {
    border: 1px solid var(--gold-dim);
    background: var(--bg-raised);
    padding: 2rem;
    display: grid;
    gap: 1.5rem;
  }

  .player__now {
    display: grid;
    grid-template-columns: 96px 1fr;
    gap: 1.5rem;
    align-items: center;
  }

  .player__cover {
    width: 96px;
    height: 96px;
    background: var(--bg-subtle);
    border: 1px solid var(--gold-dim);
    overflow: hidden;
  }

  .player__cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .player__info { min-width: 0; }

  .player__label {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
  }

  .player__title {
    font-family: var(--font-display);
    font-size: 1.5rem;
    color: var(--gold-bright);
    margin-bottom: 0.4rem;
    line-height: 1.2;
  }

  .player__time {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--text-secondary);
  }

  .player__time-sep {
    margin-inline: 0.4rem;
    color: var(--gold-dim);
  }

  .player__progress input[type='range'] {
    width: 100%;
    height: 4px;
    -webkit-appearance: none;
    appearance: none;
    background: var(--bg-subtle);
    border-radius: 2px;
    outline: none;
    cursor: pointer;
  }

  .player__progress input[type='range']::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 14px;
    height: 14px;
    background: var(--gold);
    border-radius: 50%;
    cursor: pointer;
    transition: background var(--transition);
  }

  .player__progress input[type='range']::-webkit-slider-thumb:hover {
    background: var(--gold-bright);
  }

  .player__controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .player__btn {
    width: 40px;
    height: 40px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    border: 1px solid transparent;
    transition: all var(--transition);
    border-radius: 50%;
  }

  .player__btn:hover {
    color: var(--gold-bright);
    border-color: var(--gold-dim);
  }

  .player__btn--play {
    width: 52px;
    height: 52px;
    color: var(--bg-deep);
    background: var(--gold);
  }

  .player__btn--play:hover {
    background: var(--gold-bright);
    color: var(--bg-deep);
    border-color: var(--gold-bright);
  }

  .player__volume {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-left: auto;
    color: var(--text-muted);
  }

  .player__volume input[type='range'] {
    width: 100px;
    height: 3px;
    -webkit-appearance: none;
    appearance: none;
    background: var(--bg-subtle);
    border-radius: 2px;
    outline: none;
    cursor: pointer;
  }

  .player__volume input[type='range']::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 10px;
    height: 10px;
    background: var(--gold);
    border-radius: 50%;
    cursor: pointer;
  }

  .player__playlist {
    list-style: none;
    border-top: 1px solid var(--gold-dim);
    padding-top: 1rem;
    display: grid;
    gap: 0.25rem;
    max-height: 260px;
    overflow-y: auto;
  }

  .player__track {
    width: 100%;
    display: grid;
    grid-template-columns: 2rem 1fr auto;
    gap: 1rem;
    align-items: center;
    padding: 0.6rem 0.75rem;
    font-family: var(--font-body);
    font-size: 0.95rem;
    color: var(--text-secondary);
    text-align: left;
    transition: all var(--transition);
    border-radius: 2px;
  }

  .player__track:hover {
    background: var(--bg-subtle);
    color: var(--text-primary);
  }

  .player__track.is-active {
    color: var(--gold-bright);
    background: var(--bg-subtle);
  }

  .player__track-num {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--gold-dim);
  }

  .player__track.is-active .player__track-num { color: var(--gold); }

  .player__track-title {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .player__track-dur {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-muted);
  }

  @media (max-width: 640px) {
    .player { padding: 1.25rem; }
    .player__now { grid-template-columns: 72px 1fr; gap: 1rem; }
    .player__cover { width: 72px; height: 72px; }
    .player__title { font-size: 1.15rem; }
    .player__volume { display: none; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 5. src/components/TrackCard.astro
# ═════════════════════════════════════════════════════════════════════════
FILES["src/components/TrackCard.astro"] = """\
---
interface Props {
  slug: string;
  title: string;
  cover: string;
  description: string;
  duration: string;
  releaseBase: string;
  file: string;
}

const {
  slug, title, cover, description, duration, releaseBase, file,
} = Astro.props;

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const coverUrl = `${base}${cover}`;
const downloadUrl = `${releaseBase}/${file}`;
const detailUrl = `${base}/music/${slug}`;
---

<article class="track-card">
  <a href={detailUrl} class="track-card__cover">
    <img src={coverUrl} alt={title} loading="lazy" />
  </a>

  <div class="track-card__body">
    <a href={detailUrl} class="track-card__title">{title}</a>
    <p class="track-card__desc">{description}</p>

    <div class="track-card__meta">
      <span class="track-card__dur">{duration}</span>
      <div class="track-card__actions">
        <a href={detailUrl} class="track-card__link">Текст →</a>
        <a
          href={downloadUrl}
          class="track-card__download"
          download
          data-download={slug}
        >
          ↓ Скачать
        </a>
      </div>
    </div>
  </div>
</article>

<style>
  .track-card {
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 1.5rem;
    padding: 1.25rem;
    border: 1px solid var(--gold-dim);
    background: var(--bg-raised);
    transition: all var(--transition);
  }

  .track-card:hover {
    border-color: var(--gold);
    background: var(--bg-subtle);
  }

  .track-card__cover {
    aspect-ratio: 1;
    background: var(--bg-subtle);
    border: 1px solid var(--gold-dim);
    overflow: hidden;
    display: block;
  }

  .track-card__cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 400ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  .track-card:hover .track-card__cover img {
    transform: scale(1.04);
  }

  .track-card__body {
    display: flex;
    flex-direction: column;
    min-width: 0;
  }

  .track-card__title {
    font-family: var(--font-display);
    font-size: 1.35rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    transition: color var(--transition);
    line-height: 1.2;
  }

  .track-card__title:hover { color: var(--gold-bright); }

  .track-card__desc {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.55;
    margin-bottom: 1rem;
    flex: 1;
  }

  .track-card__meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--gold-dim);
  }

  .track-card__dur {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
  }

  .track-card__actions {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  .track-card__link {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--gold);
  }

  .track-card__link:hover { color: var(--gold-bright); }

  .track-card__download {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--cyan);
  }

  .track-card__download:hover { color: var(--gold-bright); }

  @media (max-width: 640px) {
    .track-card {
      grid-template-columns: 1fr;
      gap: 1rem;
      padding: 1rem;
    }

    .track-card__cover {
      max-width: 180px;
    }

    .track-card__meta { flex-direction: column; align-items: flex-start; }
  }
</style>
"""

# ═════════════════════════════════════════════════════════════════════════
# 6. src/pages/music.astro
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/music.astro"] = """\
---
import BaseLayout from '../layouts/BaseLayout.astro';
import MusicPlayer from '../components/MusicPlayer.astro';
import TrackCard from '../components/TrackCard.astro';
import '../styles/global.css';

import tracksData from '../data/tracks.yaml';

const { tracks, release_base } = tracksData;

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
# 7. src/pages/music/[slug].astro
# ═════════════════════════════════════════════════════════════════════════
FILES["src/pages/music/[slug].astro"] = """\
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import MusicPlayer from '../../components/MusicPlayer.astro';
import '../../styles/global.css';

import tracksData from '../../data/tracks.yaml';

export async function getStaticPaths() {
  const { tracks } = tracksData;
  return tracks.map((t) => ({
    params: { slug: t.slug },
    props: { track: t, allTracks: tracks, releaseBase: tracksData.release_base },
  }));
}

const { track, allTracks, releaseBase } = Astro.props;

const lyrics = await getCollection('music', (e) => e.data.slug === track.slug);
const lyricsEntry = lyrics[0];
const { Content } = lyricsEntry
  ? await lyricsEntry.render()
  : { Content: null };

const base = import.meta.env.BASE_URL.replace(/\\/$/, '');
const coverUrl = `${base}${track.cover}`;
const downloadUrl = `${releaseBase}/${track.file}`;

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
      <MusicPlayer tracks={[track]} releaseBase={releaseBase} />
    </div>
  </section>

  {lyricsEntry && (
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
    white-space: pre-line;
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

# ═════════════════════════════════════════════════════════════════════════
# 8. public/covers/_placeholder.svg
# ═════════════════════════════════════════════════════════════════════════
FILES["public/covers/_placeholder.svg"] = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <rect width="400" height="400" fill="#13110c"/>
  <text x="200" y="210" text-anchor="middle"
        font-family="serif" font-size="64" fill="#c9a961" opacity="0.6">✶</text>
  <text x="200" y="270" text-anchor="middle"
        font-family="monospace" font-size="14" fill="#6b6353"
        letter-spacing="4">ХАРТИЯ 5.0</text>
</svg>
"""

# ═════════════════════════════════════════════════════════════════════════
# 9. public/audio/README.md
# ═════════════════════════════════════════════════════════════════════════
FILES["public/audio/README.md"] = f"""\
# Аудио

MP3-файлы **не хранятся в репозитории**. Они загружаются в GitHub Releases:

{RELEASE_BASE}

## Как обновить

1. Открой https://github.com/vamhana/hartia/releases
2. Создай новый релиз с тегом `audio-v1`
3. Загрузи 5 mp3-файлов (переименованных в латиницу без пробелов):
   - `komfortnyj-ad.mp3`
   - `upgrade-pustoty.mp3`
   - `paketik-dlya-spyashchih.mp3`
   - `na-u-yu.mp3`
   - `na-u-yu-wrapped.mp3`
4. Опубликуй релиз
5. Проверь, что ссылки работают:
   {RELEASE_BASE}/komfortnyj-ad.mp3

## Обложки

Извлекаются скриптом `scripts/extract_covers.py` в `public/covers/`.
Нужен Python-пакет `mutagen`:

    pip install mutagen
"""
# ═════════════════════════════════════════════════════════════════════════
# 10. Запись файлов
# ═════════════════════════════════════════════════════════════════════════

def write_files() -> tuple[int, int, int]:
    created = updated = skipped = 0

    for rel, content in FILES.items():
        path = ROOT / rel
        existed = path.exists()

        if DRY_RUN:
            status = "UPDATE" if existed else "CREATE"
            print(f"[{status}] {rel}")
            if existed:
                updated += 1
            else:
                created += 1
            continue

        if existed and not FORCE:
            print(f"[SKIP]   {rel}  (уже есть, нужен --force)")
            skipped += 1
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        # Нормализуем переводы строк — иначе на Windows получим CRLF
        text = content.replace("\r\n", "\n")
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"[{'UPDATE' if existed else 'CREATE'}] {rel}")
        if existed:
            updated += 1
        else:
            created += 1

    return created, updated, skipped


def main() -> int:
    if DRY_RUN:
        mode = "DRY-RUN"
    elif FORCE:
        mode = "FORCE"
    else:
        mode = "NORMAL"

    print(f"Хартия · шаг 3 (музыка) · режим: {mode}")
    print(f"Корень проекта: {ROOT}")
    print(f"Файлов в очереди: {len(FILES)}")
    print("─" * 64)

    created, updated, skipped = write_files()

    print("─" * 64)
    if DRY_RUN:
        print(f"Итого (dry-run): создать — {created}, перезаписать — {updated}")
        print("На диск ничего не записано. Убери --dry-run, чтобы применить.")
    else:
        print(f"Итого: создано — {created}, обновлено — {updated}, пропущено — {skipped}")
        if skipped and not FORCE:
            print("Часть файлов уже существует. Запусти с --force, чтобы перезаписать.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
