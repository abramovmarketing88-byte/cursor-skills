# Шаблон ТЗ / Brief

Помечать поля: CONFIRMED / INFERRED / TODO.

```markdown
# AI Seller Brief

## Business Context
- Компания, сайт, канал (Avito / …), платформа (Suvvy)
- Роль бота
- Что продаём / не продаём

## Main User Intents
- Список типичных первых сообщений

## Qualification Logic
- Large / medium / small (внутренние сигналы)
- Когда НЕ спрашивать бюджет
- Порог «от X» и что в него входит (если есть)

## Pricing Logic
- Изделие/услуга vs материал/единица
- Обязательная формулировка ориентира
- «Дорого» — как отвечать

## Data Sources
- Таблицы (колонки поиска, функции Suvvy)
- Прайс-файлы
- Адрес / география / формат (онлайн / визит)

## CRM / Handoff Logic
- Триггеры A/B/C/D
- Статус «куда» (не выдумывать id в чат)
- Telegram notification
- После вызова: продолжать чат

## Dialogue UX
- Язык, тон, длина
- Soft call / chat-only
- Лимиты вопросов

## Must-Fix Failures
- Нумерованный список из чатов/скринов

## Forbidden Behaviors
- Сводка bans

## Files To Create Or Update
- prompt, files-map, sources, suvvy-qa, csv

## Deploy Notes
- Temperature, число DQ, имена табличных функций
```

## Executive summary (3–5 строк)

Зачем бот, главный gap текущих чатов, топ-3 правила (обычно: ориентир цены, не телефон первым, chat-only).
