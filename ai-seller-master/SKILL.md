---
name: ai-seller-master
description: Analyze Avito/Suvvy seller chats, logs, PDFs, screenshots, and business notes, then design or refactor a production AI seller skill with Instructions, files-map, source-of-truth docs, Direct Questions (get_file_text), tables, CRM/Bitrix handoff, qualification, anti-hallucination bans, and deploy checklist. Use when creating, auditing, universalizing, or fixing marketplace sales bots on Suvvy.ai.
disable-model-invocation: true
---

# AI Seller Master

Единый мастер: **анализ → ТЗ → production-скилл → деплой в Suvvy**.  
Нишевые факты (цены, адрес, SKU) живут в `sources/*` конкретного бота. Здесь — **универсальная логика** с Avito + Suvvy (камень и разборы живых чатов) плюс правила платформы.

Нишевый пак (например Ein-Stein) **не удалять и не заменять** этим мастером: мастер его аудирует и расширяет.

## Справочники (читать по задаче)

| Файл | Когда |
|------|--------|
| [suvvy-platform.md](references/suvvy-platform.md) | слои знаний, DQ, CRM, каналы |
| [suvvy-prompt-rules.md](references/suvvy-prompt-rules.md) | как писать Instructions по доке Suvvy |
| [seller-logic.md](references/seller-logic.md) | ценность, soft call, large/medium/small, CRM A–D |
| [scenario-playbooks.md](references/scenario-playbooks.md) | визит, наличие, продукт, «дорого», out of scope |
| [instructions-template.md](references/instructions-template.md) | полный скелет ROLE…IMPORTANT |
| [hard-bans-universal.md](references/hard-bans-universal.md) | запреты в Restrictions |
| [prompt-pack.md](references/prompt-pack.md) | files-map, wrap, Excel |
| [table-setup.md](references/table-setup.md) | CSV, две функции, поиск |
| [failure-patterns.md](references/failure-patterns.md) | регрессии из живых чатов |
| [brief-template.md](references/brief-template.md) | ТЗ CONFIRMED/INFERRED/TODO |
| [wrap_sources.py](references/wrap_sources.py) / [build_xlsx.py](references/build_xlsx.py) | синхронизация DQ |
| [examples.md](examples.md) | сценарии применения |

Документация Suvvy: https://docs.suvvy.ai/ru/llms.txt

## Когда включать

Переписки Авито, логи бота, PDF/скрины, «почему не находит в таблице», промпт Suvvy, Direct Questions, Bitrix/воронка, квалификация, телефон, chat-only, антигаллюцинации, новый бот с нуля.

## Источник правды

Отвечать **только** из:

1. Instructions (`prompt.md` / `prompt-suvvy-paste.md`)
2. Direct Questions — `get_file_text("Exact Title")`, заголовок байт-в-байт, тумблер вкл
3. Табличные функции (CSV/XLS/Sheets)
4. Факты клиента **во всей** переписке
5. Публичные ссылки каталога компании (навигация, не выдуманные цены)

Нет в источниках → не выдумывать → менеджер. Клиенту **не** писать «не найден в базе» / «такого нет».

Конфликт промпт vs DQ: **промпт побеждает**; факты прайса/адреса — в DQ/таблице, не дублировать противоречиво.

---

## Phase 1 — Discovery

Прочитать **все** вложения: чаты, скрины, PDF (включая картинки внутри), TXT, текущий промпт, список DQ, таблицы, скрины UI Suvvy (Integrations, имена функций).

Пометить: **CONFIRMED** / **INFERRED** / **TODO**.

Снять:

| Блок | Что извлечь |
|------|-------------|
| Бизнес | роль, канал, продукт vs услуга, out of scope, сайт |
| Интенты | цена, наличие, «где посмотреть», услуга, «дорого», только чат |
| Квалификация | large / medium / small **внутри**; клиенту ярлыки не говорить |
| Экономика | материал vs под ключ; порог «от X»; что входит; формулу клиенту не говорить |
| Данные | таблица, прайс, адрес, каталог, колонки поиска |
| CRM | A–D, один раз за диалог, после вызова **продолжать чат**; ID через шестерёнку |
| Телефон | Notification DQ; не переспрашивать; после валидного номера не раздувать анкету |
| Провалы | телефон вместо ответа, дубли, тишина, пропуск таблицы, CRM слишком поздно |

Группы сбоев: логика / дыры в знаниях / приоритеты / тон / интеграции / имена функций.

---

## Phase 2 — Architecture

```text
skill-name/
├── SKILL.md                 # disable-model-invocation: true у нишевой базы
├── prompt.md
├── prompt-suvvy-paste.md    # → Instructions
├── files-map.md
├── sources/                 # править здесь
│   ├── qualification-by-scale.md
│   ├── pricing-factors.md
│   ├── warehouse-address.md (или coverage)
│   ├── availability-rules.md
│   ├── catalog-assortment.md
│   ├── scenario-playbooks.md
│   ├── chat-only-mode.md
│   ├── hard-bans.md
│   ├── bitrix-funnel-stage.md   # CRM DQ
│   ├── notification-telegram.md
│   ├── stock-prices.md          # если есть listed unit prices
│   ├── follow-ups-reference.md  # НЕ грузить в бота
│   └── *.csv
└── suvvy-qa/
    ├── wrap_sources.py
    ├── build_xlsx.py
    └── NN-*.md
```

Оркестрация в промпте. Факты в `sources/*`. Ситуация → файл → DQ в `files-map.md`.

---

## Phase 3 — Реализация

1. Brief по [brief-template.md](references/brief-template.md).
2. `prompt-suvvy-paste.md` из [instructions-template.md](references/instructions-template.md); цифры и имена функций — из ниши.
3. `#WORKING WITH FUNCTIONS`: когда какой `get_file_text` и какая таблица (primary → fallback).
4. `#RESTRICTIONS` из [hard-bans-universal.md](references/hard-bans-universal.md) + нишевые.
5. `sources/*` → `suvvy-qa/*` через wrap. Не править qa в одиночку.
6. CSV UTF-8 **без BOM**; поиск токеном из **всего чата**; `search_text` + алиасы; см. [table-setup.md](references/table-setup.md).
7. Каждый повторный сбой из чатов → ban в hard-bans **и** Restrictions.
8. Писать Instructions по [suvvy-prompt-rules.md](references/suvvy-prompt-rules.md): без противоречий, запреты утвердительные, «шаг за шагом если ещё не известно».

---

## Phase 4 — Деплой Suvvy

1. [app.suvvy.ai](https://app.suvvy.ai/) → **Instructions** ← `prompt-suvvy-paste.md` (заголовки UI можно адаптировать, **правила не резать**).
2. **База знаний → Вопрос — ответ** ← `suvvy-qa/*` или Excel. Тумблеры **вкл**. Title = вызов в промпте. **< ~50** DQ.
3. Follow-ups-reference **не** импортировать в бота.
4. Таблица: один CSV, при необходимости **два имени функции**, описание LIKE, «только токен».
5. CRM: Integrations на DQ (статус «куда» + свободный оператор) **или** одно LLM-действие с тем же смыслом A–D. Не три параллельных механизма.
6. Temperature **0–0.3**.
7. Платформенные фоллоу-апы Suvvy не дублировать с отдельным приложением дожимов. Бот не обещает «напомню».
8. Регрессии: [failure-patterns.md](references/failure-patterns.md).

---

## Поведение бота (кратко)

Полностью: seller-logic + scenario-playbooks + instructions-template.

1. Ценность первой. Весь диалог как один контекст.
2. Не телефон вместо ответа на факт-вопрос.
3. Soft call: «удобно созвониться?» → номер после «да» или если уже прислали. Не повторять запрос номера.
4. Chat-only — полный сервис в чате.
5. Large → CRM **сразу**, без вопроса бюджета. Medium/small → мягкий «от X» → CRM на согласие.
6. После CRM продолжать писать. Клиенту не говорить про воронку.
7. После **валидного телефона**: Notification DQ; не раздувать новую анкету.
8. Не дублировать смысл за ход. Не тупик «всё на заказ».
9. ≤5 уточнений за диалог; ≤2 в сообщении.
10. Ярлыки масштаба — только внутри.

---

## Deliverables

A) ТЗ  
B) Production pack + чеклист деплоя  
C) Список регрессий из живых чатов
