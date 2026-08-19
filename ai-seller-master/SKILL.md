---
name: ai-seller-master
description: Analyze sales chats, logs, PDFs, screenshots, and business notes, then design or refactor a production AI seller skill with prompt, files map, source-of-truth docs, Direct Questions, tables, and CRM handoff rules. Use when creating, auditing, universalizing, or fixing Avito/Suvvy seller bots, marketplace sales prompts, anti-hallucination knowledge packs, or business-specific seller skills.
disable-model-invocation: true
---

# AI Seller Master

Единый мастер-скилл для ИИ-продавцов: анализ вводных → ТЗ → production-скилл (`prompt.md`, `files-map.md`, `sources/*`, `suvvy-qa/*`).

## Что делает

1. Разбирает переписки, логи, PDF, скриншоты, заметки.
2. Собирает ТЗ (квалификация, цены, CRM, запреты).
3. Собирает или чинит production-скилл без галлюцинаций.
4. Чинит повторяющиеся провалы живых чатов явными банами и сценариями.

## Когда использовать

Анализ переписок, ТЗ для бота, промпт Suvvy, карта файлов, Direct Questions, CRM/Bitrix, правка существующего seller-скилла.

## Workflow

### Phase 1 — Discovery

Извлечь: бизнес и канал, товары/услуги, интенты, квалификацию, цены, источники данных, CRM/handoff, запреты, повторяющиеся сбои.

Группировать сбои: логика, пробелы в знаниях, приоритеты, тон/UX, интеграции.

### Phase 2 — Architecture

```text
skill-name/
├── SKILL.md
├── prompt.md
├── prompt-*.md
├── files-map.md
├── sources/
└── suvvy-qa/
```

### Phase 3 — Implementation

1. Оркестрация — в `prompt.md`.
2. Факты — в `sources/*`.
3. Карта ситуаций — в `files-map.md`.
4. Direct Questions — в `suvvy-qa/*` с точными заголовками.
5. Живые данные — в таблицах, не в прозе промпта.
6. Повторяющиеся ошибки — в bans / playbooks.

## Поведение бота-продавца

1. Сначала ответ, потом квалификация.
2. Не выдумывать цены, сроки, скидки, гарантии, остатки.
3. Только утверждённые источники и таблицы.
4. Спрашивать только недостающие факты.
5. Квалифицированный лид → CRM/handoff, диалог продолжается, пока не подключится менеджер.
6. Chat-only — без давления на звонок.

## Универсальные правила

- Весь контекст переписки.
- Не переспрашивать уже сказанное.
- Отличать цену изделия и цену материала.
- Сначала ценность, потом телефон.
- Lookup vs handoff менеджеру.
- Наличие: токен → колонки поиска → fallback → эскалация.
- CRM: точные триггеры, один раз за диалог, что делать после вызова.

## Минимум источников

- scope услуг/товаров
- pricing / estimate
- qualification
- availability / coverage
- FAQ / процесс
- objections
- CRM handoff
- notifications
- hard bans

## Deliverables

### A) Brief / TZ

```markdown
# AI Seller Brief

## Business Context
## Main User Intents
## Qualification Logic
## Pricing Logic
## Data Sources
## CRM / Handoff Logic
## Must-Fix Failures
## Forbidden Behaviors
## Files To Create Or Update
```

### B) Production pack

`SKILL.md`, `prompt.md`, `files-map.md`, `sources/*`, `suvvy-qa/*`

## Maintenance

- Оркестрация в `prompt.md`, факты в `sources/*`.
- Заголовки Direct Questions в Suvvy — точные.
- Повторный сбой в чатах → явный ban или сценарий.
- Не патчить промпт в обход source-of-truth.

Нишевые скиллы (например Ein-Stein) не дублируют этот мастер: мастер аудирует и правит их структуру.
