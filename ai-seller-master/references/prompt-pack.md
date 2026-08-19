# Production-пак файлов

## Назначение файлов

| Файл | Куда в Suvvy | Правило |
|------|----------------|---------|
| `prompt.md` | эталон логики в репо | Можно чуть подробнее paste |
| `prompt-suvvy-paste.md` | **Instructions** | Секции ROLE/GOALS/… |
| `files-map.md` | агенту Cursor + людям | ситуация → sources + DQ title |
| `sources/*.md` | истина | Править здесь |
| `suvvy-qa/*.md` | Вопрос — ответ | Те же тексты, exact title |
| CSV | Таблицы | UTF-8 без BOM |
| `hard-bans.md` | дубль в Restrictions | Чеклист |

## Шаблон files-map.md

```markdown
# Files map

Не отвечать фактами из памяти.

| Situation | Open these files | Suvvy Direct Question (exact title) |
|-----------|------------------|-------------------------------------|
| Main behavior | prompt.md | — (Instructions) |
| Qualification | sources/qualification-*.md | `Qualification …` |
| Price | sources/pricing-*.md | `Pricing …` |
| Stock / coverage | sources/*-rules.md | `… Rules` + table functions |
| Visit / address | sources/address.md | `Warehouse Address` / analog |
| Chat-only | sources/chat-only-mode.md | `Chat Only Mode` |
| Scenarios | sources/scenario-playbooks.md | `Scenario Playbooks` |
| CRM | sources/crm-handoff.md | `Bitrix Funnel Stage` (или аналог) |
| Phone → notify | sources/notification-telegram.md | `Notification in telegram` |
| Bans | sources/hard-bans.md | — |
| Unknown | — | Don't invent; manager |

Live data: table function names, search column order, empty → manager.
```

Заголовки DQ **латиницей стабильнее** (меньше опечаток в `get_file_text`).

## Синхронизация sources → suvvy-qa

Скрипт `wrap_sources.py`: MAP список `(qa_file, source_file, Exact Title)`.

Правило: правка только в `sources/`, потом wrap, потом вставка в Suvvy. Не править qa в одиночку.

## Что писать в prompt WORKING WITH FUNCTIONS

Для каждого DQ: «если клиент спрашивает X → get_file_text("Title")».

Для таблиц: порядок функций, колонки, токен, max rows, запрет invent.

Для CRM: приоритет A–D, once per dialogue, continue chat.

Для телефона: Notification DQ **и** не повторять запрос номера.

## SKILL.md нишевого бота (короткий)

Как Ein-Stein:

1. Читать prompt.
2. Ситуация → files-map → sources.
3. Нет в файлах → не выдумывать.
4. Деплой: paste Instructions + DQ on + таблицы.

`disable-model-invocation: true` у нишевого пака, если это только база, не авто-скилл агента.

## Excel / импорт

`build_xlsx.py` собирает knowledge base. После смены прайса — пересборка и заливка.

## Имена табличных функций

В промпте и в UI Suvvy — **одинаковые**. Если UI переименовал — либо править промпт, либо второе подключение того же CSV под старым именем (оба вызова в промпте).

## wrap_sources.py

Шаблон: [wrap_sources.py](wrap_sources.py). MAP: `(qa_file, source_file, Exact Title)`.  
Правка только `sources/` → `python wrap_sources.py` → вставка в Suvvy.

Формат qa (см. wrap_sources.py): заголовок `# Suvvy Direct Question…`, строка `**Title (exact):** \`Title\``, затем fenced body из `sources/` без дублирующего H1.

Заголовки DQ латиницей стабильнее (меньше опечаток в `get_file_text`).

## Excel импорт

Шаблон: [build_xlsx.py](build_xlsx.py). Колонки: Title, Search Title, Content, Used=True.  
`SKIP` = follow-ups. После смены sources: wrap → build_xlsx → импорт в «Вопрос — ответ».

## Notification DQ

Файл `sources/notification-telegram.md`, title ровно как в промпте (часто `Notification in telegram`). Может не входить в wrap MAP, если тело собирается иначе — тогда всё равно держать в files-map.

## Нишевый SKILL.md

1. Читать prompt.  
2. Ситуация → files-map → sources.  
3. Нет в файлах → не выдумывать.  
4. Деплой: paste Instructions + DQ on + таблицы.  
`disable-model-invocation: true`.
