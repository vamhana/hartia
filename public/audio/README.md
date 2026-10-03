# Аудио

MP3-файлы **не хранятся в репозитории**. Они загружаются в GitHub Releases:

https://github.com/vamhana/hartia/releases/download/audio-v1

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
   https://github.com/vamhana/hartia/releases/download/audio-v1/komfortnyj-ad.mp3

## Обложки

Извлекаются скриптом `scripts/extract_covers.py` в `public/covers/`.
Нужен Python-пакет `mutagen`:

    pip install mutagen
