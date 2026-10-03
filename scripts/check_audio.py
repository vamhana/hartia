#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Проверка аудиофайлов, путей и компонентов.

Запуск:
    python scripts/check_audio.py
"""

import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

AUDIO_DIR = ROOT / "public" / "audio"
COVERS_DIR = ROOT / "public" / "covers"
TRACKS_TS = ROOT / "src" / "data" / "tracks.ts"
PLAYER = ROOT / "src" / "components" / "MusicPlayer.astro"
CARD = ROOT / "src" / "components" / "TrackCard.astro"


def main() -> int:
    print("── 1. Файлы в public/audio/ ──")
    if not AUDIO_DIR.exists():
        print(f"  ✗ Папка не найдена: {AUDIO_DIR}")
        return 1

    mp3s = sorted(AUDIO_DIR.glob("*.mp3"))
    if not mp3s:
        print("  ✗ Нет mp3-файлов")
        return 1

    for mp3 in mp3s:
        size_mb = mp3.stat().st_size / 1024 / 1024
        print(f"  ✓ {mp3.name} ({size_mb:.1f} МБ)")

    print()
    print("── 2. Файлы в public/covers/ ──")
    if not COVERS_DIR.exists():
        print(f"  ✗ Папка не найдена: {COVERS_DIR}")
    else:
        covers = sorted(COVERS_DIR.glob("*"))
        if not covers:
            print("  ✗ Нет обложек")
        for c in covers:
            print(f"  ✓ {c.name}")

    print()
    print("── 3. Соответствие tracks.ts и файлов ──")
    if not TRACKS_TS.exists():
        print(f"  ✗ Нет {TRACKS_TS}")
        return 1

    ts = TRACKS_TS.read_text(encoding="utf-8")
    files_in_ts = re.findall(r"file:\s*'([^']+)'", ts)
    missing = []
    for f in files_in_ts:
        if not (AUDIO_DIR / f).exists():
            missing.append(f)
            print(f"  ✗ Нет файла для '{f}'")
        else:
            print(f"  ✓ {f}")

    print()
    print("── 4. Проверка MusicPlayer.astro ──")
    if not PLAYER.exists():
        print(f"  ✗ Нет {PLAYER}")
        return 1

    player_src = PLAYER.read_text(encoding="utf-8")

    # Ищем строку формирования src
    src_match = re.search(r"src:\s*`([^`]+)`", player_src)
    if src_match:
        pattern = src_match.group(1)
        print(f"  Текущий шаблон src: `{pattern}`")
        if "/audio/" not in pattern:
            print("  ⚠ В шаблоне нет '/audio/' — плеер ищет файлы не в public/audio/")
        else:
            print("  ✓ Шаблон содержит '/audio/'")
    else:
        print("  ⚠ Не удалось найти строку 'src:' в MusicPlayer.astro")

    print()
    print("── 5. Проверка TrackCard.astro ──")
    if not CARD.exists():
        print(f"  ✗ Нет {CARD}")
        return 1

    card_src = CARD.read_text(encoding="utf-8")
    dl_match = re.search(r"downloadUrl\s*=\s*`([^`]+)`", card_src)
    if dl_match:
        pattern = dl_match.group(1)
        print(f"  Текущий шаблон downloadUrl: `{pattern}`")
        if "/audio/" not in pattern:
            print("  ⚠ В шаблоне нет '/audio/' — скачивание пойдёт не туда")
        else:
            print("  ✓ Шаблон содержит '/audio/'")
    else:
        print("  ⚠ Не удалось найти 'downloadUrl' в TrackCard.astro")

    print()
    print("── Итог ──")
    if missing:
        print(f"  ✗ Не хватает файлов: {missing}")
        print("    Скопируй их в public/audio/ с правильными именами.")
    else:
        print("  ✓ Все файлы на месте")
    print()
    print("Если в шаблонах src/downloadUrl нет '/audio/', нужно")
    print("заменить их на:")
    print("  MusicPlayer:  src: `${audioBase}/audio/${t.file}`")
    print("  TrackCard:    const downloadUrl = `${base}/audio/${file}`")
    print()
    print("(audioBase и base уже содержат префикс /hartia для продакшена)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())