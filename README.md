# Album Library Static Site Generator

A deterministic, AI-assisted pipeline that converts a local Markdown album library into a polished Astro website, enriches it with high-quality cover art, and generates professional analytical guides.

## 🚀 Быстрый старт

### 1. Требования
- **Node.js**: v20+
- **Python**: v3.10+
- **Virtual Environment**: venv в `~/venv/cover-api` с установленным `requests`.

### 2. Подключите вашу коллекцию
Проект настроен на работу с вашей папкой в `content/my_collection/`. Формат файлов:
```markdown
# Artist — Album (Year)
Текст вашего гида здесь.
```

### 3. Автоматизация (Gemini Skill)
Для полного цикла используйте установленный навык:
```bash
/skills reload
Запусти оркестрацию альбомов через новый скилл
```

Скилл сам:
1. Просканирует коллекцию.
2. Скачает обложки (до 5 попыток с ИИ-оптимизацией при ошибках).
3. Запустит локальное превью сайта.
4. После вашего подтверждения сделает коммит и пуш.

## 📂 Структура проекта

- `/content/my_collection/`: Ваши Markdown-файлы.
- `/public/covers/`: Скачанные обложки.
- `/scripts/`: Python-инструменты.
- `/site/`: Исходный код Astro.
- `/state/`: Каталог и логи.
- `/.gemini/skills/album-orchestrator`: Логика автоматизации.

## 🛠 Ручные команды

1. **Сканирование**: `python scripts/scan_albums.py --input content/my_collection --output state/catalog.json`
2. **Оркестрация**: `python scripts/orchestrator.py`
3. **Превью**: `cd site && npm run dev`

## 🚢 Деплой

Проект включает GitHub Actions в `.github/workflows/deploy.yml`. 
После пуша в `main` сайт автоматически соберется и опубликуется на GitHub Pages.

## ⚖️ License
MIT
