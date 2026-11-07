# Хартия 5.0

[![Сайт](https://img.shields.io/badge/сайт-vamhana.github.io/hartia-blue)](https://vamhana.github.io/hartia/)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)

**Полный текст Хартии и его web-версия.**

- **Читать онлайн:** <https://vamhana.github.io/hartia/>
- **Исходный текст:** [charter.md](charter.md)
- **Обсуждение:** [GitHub Discussions](https://github.com/vamhana/xartia/discussions) · [Telegram](https://t.me/hartia_5)

## Что это

Хартия 5.0 — свод принципов, ролей и процедур, по которым живёт
коллектив XartIA. Ядро Хартии реализовано в коде:
[vamhana/xartia](https://github.com/vamhana/xartia).

Сайт собирается из `charter.md` скриптом `scripts/parse_readme.py` →
`src/content/charter/*.md` → Astro → GitHub Pages.

## Структура

- **КНИГИ** — крупные разделы (I, II, …).
- **ЧАСТИ** — подразделы внутри книг.
- **СТАТЬИ** — минимальные единицы текста, с номерами (например, 5.2.1).

## Как обновить контент

1. Править `charter.md` (не README).
2. `python scripts/parse_readme.py --force`
3. (если структура книг/частей изменилась) `python scripts/step_04_charter_pages.py`
4. Закоммитить `charter.md` + `src/content/charter/` + `src/pages/charter/`.
5. Push в `main` → GitHub Actions задеплоит.

## Лицензия

AGPL-3.0. Текст Хартии — общее достояние.