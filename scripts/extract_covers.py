#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Извлекает обложки из mp3-файлов в public/covers/.

Использует mutagen. Если его нет:
    pip install mutagen

Запуск:
    python scripts/extract_covers.py
    python scripts/extract_covers.py --dry-run
"""

import sys
from pathlib import Path

try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import APIC
except ImportError:
    print("[ERR] Нужен mutagen. Установи: pip install mutagen")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "public" / "audio"
COVERS_DIR = ROOT / "public" / "covers"
DRY_RUN = "--dry-run" in sys.argv


def extract(mp3_path: Path) -> tuple[bool, str]:
    """Возвращает (успех, сообщение)."""
    try:
        audio = MP3(str(mp3_path))
    except Exception as e:
        return False, f"не читается: {e}"

    if audio.tags is None:
        return False, "нет ID3-тегов"

    covers = [v for v in audio.tags.values() if isinstance(v, APIC)]
    if not covers:
        return False, "нет APIC (обложки)"

    # Берём первую (обычно front cover)
    apic = covers[0]
    ext = "jpg" if apic.mime == "image/jpeg" else (
        "png" if apic.mime == "image/png" else "bin"
    )
    stem = mp3_path.stem.lower().replace(" ", "-")
    out = COVERS_DIR / f"{stem}.{ext}"

    if DRY_RUN:
        return True, f"[dry] {out.name} ({len(apic.data)} B, {apic.mime})"

    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    out.write_bytes(apic.data)
    return True, f"{out.name} ({len(apic.data)} B)"


def main() -> int:
    if not AUDIO_DIR.exists():
        print(f"[ERR] нет папки: {AUDIO_DIR}")
        print("Сначала положи mp3 в public/audio/")
        return 1

    mp3s = sorted(AUDIO_DIR.glob("*.mp3"))
    if not mp3s:
        print(f"[ERR] в {AUDIO_DIR} нет mp3")
        return 1

    print(f"Найдено mp3: {len(mp3s)}")
    if DRY_RUN:
        print("Режим: --dry-run")
    print()

    ok = fail = 0
    for mp3 in mp3s:
        success, msg = extract(mp3)
        mark = "✓" if success else "✗"
        print(f"  {mark} {mp3.name}: {msg}")
        if success:
            ok += 1
        else:
            fail += 1

    print()
    print(f"Итог: успешно {ok}, не удалось {fail}.")
    if fail and not DRY_RUN:
        print("Файлы без обложки — просто используй плейсхолдер (public/covers/_placeholder.svg).")
    return 0


if __name__ == "__main__":
    sys.exit(main())