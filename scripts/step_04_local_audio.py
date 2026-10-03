#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Переносит mp3 из релиза в public/audio/ и обновляет tracks.ts.

Запуск:
    python scripts/step_04_local_audio.py --dry-run
    python scripts/step_04_local_audio.py
    python scripts/step_04_local_audio.py --force
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORCE = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

# Новый базовый путь — локальные файлы в public/audio/
LOCAL_BASE = "/audio"

FILES: dict[str, str] = {}

# ═════════════════════════════════════════════════════════════════════════
# tracks.ts — локальные пути вместо GitHub Releases
# ═════════════════════════════════════════════════════════════════════════
FILES["src/data/tracks.ts"] = """\
export interface Track {
  slug: string;
  title: string;
  file: string;
  duration: string;
  year: number;
  cover: string;
  tags: string[];
  description: string;
}

// Локальные файлы в public/audio/ — нет CORS-проблем
export const release_base = '';

export const tracks: Track[] = [
  {
    slug: 'komfortnyj-ad',
    title: 'Комфортный ад',
    file: 'komfortnyj-ad.mp3',
    duration: '4:20',
    year: 2026,
    cover: '/covers/komfortnyj-ad.jpg',
    tags: ['phonk', 'hyperpop', 'anti-consumerism'],
    description: 'Пробуждение от сна системы. Манифест тех, кто устал быть расходным материалом.',
  },
  {
    slug: 'upgrade-pustoty',
    title: 'Апгрейд пустоты',
    file: 'upgrade-pustoty.mp3',
    duration: '4:55',
    year: 2026,
    cover: '/covers/upgrade-pustoty.png',
    tags: ['phonk', 'industrial', 'transformation'],
    description: 'После взрыва не строю стены. Взрыв — это диагноз. О сборке себя из пепла.',
  },
  {
    slug: 'paketik-dlya-spyashchih',
    title: 'Пакетик для спящих',
    file: 'paketik-dlya-spyashchih.mp3',
    duration: '3:48',
    year: 2026,
    cover: '/covers/paketik-dlya-spyashchih.jpg',
    tags: ['phonk', 'satire', 'awakening'],
    description: 'О тех, кто заваривает собственный сон. Одуванчик против пакетика.',
  },
  {
    slug: 'na-u-yu',
    title: 'На-у-ю',
    file: 'na-u-yu.mp3',
    duration: '3:15',
    year: 2026,
    cover: '/covers/na-u-yu.jpg',
    tags: ['phonk', 'banks', 'freedom'],
    description: 'Все банки в ряд намотаю. Прощание с долговой системой.',
  },
  {
    slug: 'na-u-yu-wrapped',
    title: 'Na-U-Yu Wrapped',
    file: 'na-u-yu-wrapped.mp3',
    duration: '3:15',
    year: 2026,
    cover: '/covers/na-u-yu-wrapped.jpg',
    tags: ['phonk', 'banks', 'english'],
    description: 'English version. All the banks in a row I\\'ll wrap.',
  },
];

export default { release_base, tracks };
"""

def main() -> int:
    if not ROOT.exists():
        print(f"[ERR] нет {ROOT}")
        return 1

    print(f"Проект: {ROOT}")
    if DRY_RUN: print("Режим: --dry-run")
    if FORCE: print("Режим: --force")
    print()

    print("── Файлы ──")
    for rel, content in FILES.items():
        full = ROOT / rel
        if full.exists() and not FORCE:
            try:
                if full.read_text(encoding="utf-8") == content:
                    print(f"[same]  {rel}")
                    continue
            except Exception:
                pass
            print(f"[skip]  {rel}")
            continue
        if DRY_RUN:
            print(f"[dry]   {rel} ({len(content)} B)")
            continue
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        print(f"[write] {rel} ({len(content)} B)")

    print()
    print("Дальше:")
    print("  1. Скопируй все 5 mp3 в public/audio/")
    print("  2. npm run dev")
    print("  3. Открой http://localhost:4321/hartia/music")
    print()
    print("  git add .")
    print('  git commit -m "Local audio files, fix CORS"')
    print("  git push")
    print()
    return 0

if __name__ == "__main__":
    sys.exit(main())