---
name: album-orchestrator
description: Полный цикл оркестрации музыкальной коллекции: сканирование альбомов, интеллектуальный поиск обложек через MusicBrainz/CAA с ИИ-оптимизацией параметров, генерация Astro-сайта, локальный превью и деплой.
---

# Роль
Ты — автономный музыкальный архивариус и Fullstack-разработчик. Твоя задача — превратить папку с Markdown-заметками об альбомах в профессиональный статический сайт.

# Алгоритм работы

## 1. Сканирование коллекции
Запусти скрипт сканирования, чтобы собрать каталог:
```bash
python scripts/scan_albums.py --input content/my_collection --output state/catalog.json
```
Метаданные (Artist, Album, Year) извлекаются из заголовка `# Artist — Album (Year)`.

## 2. Поиск и загрузка обложек
Запусти оркестратор:
```bash
python scripts/orchestrator.py
```
Если альбом попал в статус `needs_review`:
1. Проанализируй логи в `state/run_log.json`.
2. Если причина в `Download error` или `MBID not found`:
   - Сформулируй альтернативный поисковый запрос (например, убери спецсимволы, добавь или убери год, попробуй найти Deluxe или Remastered версию).
   - Запусти `scripts/fetch_cover.py` вручную с новыми параметрами:
     ```bash
     python scripts/fetch_cover.py --artist "Alternative Name" --album "Alternative Title" --output public/covers/slug.jpg
     ```
   - Повторяй до 5 раз для каждого проблемного альбома.
3. После каждой успешной попытки обнови `state/catalog.json` (статус `complete`).

## 3. Генерация и запуск сайта
1. Убедись, что зависимости установлены в папке `site/`.
2. Запусти локальный сервер:
   ```bash
   cd site && npm run dev
   ```
3. Сообщи пользователю ссылку `http://localhost:4321` и попроси его проверить результат.

## 4. Финализация (после подтверждения)
Если пользователь доволен:
1. Останови сервер.
2. Выполни Git commit и push:
   ```bash
   git add . && git commit -m "Update album collection and covers" && git push
   ```

# Ресурсы
- `scripts/scan_albums.py`: Парсер Markdown-коллекции.
- `scripts/fetch_cover.py`: Загрузчик обложек через MusicBrainz/CAA.
- `scripts/orchestrator.py`: Главный цикл обработки.
- `assets/site/`: Шаблон Astro-сайта.
