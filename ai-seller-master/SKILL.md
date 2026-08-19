---
name: ai-seller-master
description: Analyze Avito/Suvvy seller chats, logs, PDFs, screenshots, and business notes, then design or refactor a production AI seller skill with Instructions, files-map, source-of-truth docs, Direct Questions (get_file_text), tables, CRM/Bitrix handoff, qualification, anti-hallucination bans, and deploy checklist. Use when creating, auditing, universalizing, or fixing marketplace sales bots on Suvvy.ai.
disable-model-invocation: true
---

# AI Seller Master

Единый мастер: **анализ → ТЗ → production-скилл → деплой в Suvvy**.  
Нишевые факты (цены, адрес, SKU) живут в `sources/*` конкретного бота. Здесь — **универсальная логика**, проверенная на Avito + Suvvy (камень, бухгалтерия и разборы живых чатов).

Перед работой прочитай нужные справочники:

- [suvvy-platform.md](references/suvvy-platform.md) — платформа Suvvy
- [seller-logic.md](references/seller-logic.md) — диалог, квалификация, CRM
- [prompt-pack.md](references/prompt-pack.md) — структура файлов и синхронизация
- [failure-patterns.md](references/failure-patterns.md) — живые провалы → баны
- [brief-template.md](references/brief-template.md) — шаблон ТЗ

## Когда включать

Переписки Авито, логи бота, PDF/скрины, «почему не находит в таблице», промпт Suvvy, Direct Questions, Bitrix/воронка, квалификация, телефон, chat-only, антигаллюцинации.

## Жёсткое правило источника правды

Бот (и ты при правке промпта) отвечает **только** из:

1. Instructions (`prompt.md` / `prompt-suvvy-paste.md`)
2. Direct Questions через `get_file_text("Exact Title")` — заголовок **байт-в-байт**
3. Табличные функции (CSV)
4. Явные факты клиента **во всей** переписке
5. Публичные каталожные ссылки компании (навигация, не выдуманные цены)

Нет в источниках → не выдумывать → эскалация менеджеру. Клиенту **не** писать «не найден в базе».

---

## Phase 1 — Discovery

Прочитать **все** вложения: чаты, скрины, PDF (включая картинки), TXT, текущий промпт, таблицы.

Разделить: **CONFIRMED** / **INFERRED** / **TODO**.

Снять:

| Блок | Что извлечь |
|------|-------------|
| Бизнес | роль, канал (Avito), продукт vs услуга, out of scope |
| Интенты | цена, наличие, «где посмотреть», услуга, «дорого», только чат |
| Квалификация | large / medium / small **внутри**; клиенту ярлыки не говорить |
| Цены | изделие/услуга «от» vs материал/м²; что входит |
| Данные | таблица, прайс, адрес, каталог |
| CRM | когда двигать стадию, один раз за диалог, после вызова **продолжать чат** |
| Провалы | телефон вместо ответа, дубли, тишина, повтор номера, пропуск таблицы |

Группы сбоев: логика / дыры в знаниях / приоритеты / тон / интеграции.

---

## Phase 2 — Architecture

```text
skill-name/
├── SKILL.md
├── prompt.md
├── prompt-suvvy-paste.md    # в Instructions Suvvy
├── files-map.md
├── sources/                 # править здесь
│   ├── qualification-*.md
│   ├── pricing-*.md
│   ├── scenario-playbooks.md
│   ├── chat-only-mode.md
│   ├── hard-bans.md
│   ├── crm-handoff.md       # или bitrix-funnel-stage.md
│   ├── notification-telegram.md
│   └── tables / csv
└── suvvy-qa/                # вставка в «Вопрос — ответ»
    ├── wrap_sources.py
    └── *.md
```

Оркестрация в промпте. Факты в `sources/*`. Ситуация → файл → DQ в `files-map.md`.

---

## Phase 3 — Реализация

1. Собрать/обновить `prompt-suvvy-paste.md` с секциями Suvvy: `#ROLE` `#GOALS` `#GREETING` `#RESPONSE LANGUAGE` `#RESPONSE STYLE` `#LOGIC` `#WORKING WITH FUNCTIONS` `#RESTRICTIONS` `#IMPORTANT`.
2. В `#WORKING WITH FUNCTIONS` прописать **когда** вызывать каждый `get_file_text("…")` и таблицы.
3. Синхронизировать `sources/*` → `suvvy-qa/*` (скрипт wrap).
4. Живые остатки/прайс — CSV UTF-8 **без BOM**, поиск по токену из **всего чата**, колонка `search_text` + алиасы.
5. Каждый повторный сбой из чатов → явный ban в `hard-bans.md` **и** в `#RESTRICTIONS`.

Детали: [prompt-pack.md](references/prompt-pack.md), [suvvy-platform.md](references/suvvy-platform.md).

---

## Phase 4 — Деплой Suvvy (чеклист)

1. [app.suvvy.ai](https://app.suvvy.ai/) → **Instructions** ← тело `prompt-suvvy-paste.md` (заголовки ROLE/GOALS можно адаптировать под UI, **правила не резать**).
2. **База знаний → Вопрос — ответ** ← `suvvy-qa/*` или Excel. Тумблеры **вкл**. Заголовки = вызовы в промпте. Держать блок **тонким** (ориентир **< ~50** записей).
3. Таблица(и): одна CSV, при необходимости **два имени функции** (primary + fallback), описание поиска в UI, LIKE без регистра.
4. CRM: либо Integrations на DQ (смена статуса + оператор), либо LLM-действие с описанием «когда вызывать»; ID сущности — **шестерёнка**, не руками.
5. Temperature **0–0.3**.
6. Follow-ups / дожимы — **не** в этом боте (отдельное приложение). Не обещать напоминания.
7. Прогнать регрессии из [failure-patterns.md](references/failure-patterns.md).

---

## Универсальное поведение бота

Полная логика: [seller-logic.md](references/seller-logic.md).

Кратко:

1. **Ценность первой.** Ответ на вопрос → потом квалификация / soft call.
2. **Весь диалог.** Размеры, товар, телефон могут быть в разных сообщениях.
3. **Не телефон вместо ответа** (цена, наличие, адрес, «как считается»).
4. Soft call: сначала «удобно созвониться?», номер — после «да» или если уже прислали. **Не спрашивать номер повторно.**
5. Chat-only («пишите здесь», «без звонка», «на авито») — без давления на звонок.
6. Квалификация: large → CRM **сразу** (структурно дорогой заказ); medium/small → мягкий чек «от X» → CRM на согласие.
7. После CRM **продолжать** квалифицировать. Клиенту не говорить про воронку/CRM.
8. Не дублировать одно и то же за ход. Не обрывать диалог корпоративным шаблоном без следующего вопроса.
9. ≤5 уточняющих вопросов за диалог; ≤2 связанных в одном сообщении; уже отвеченное не повторять.
10. Ярлыки «крупный/средний заказ» — **только внутри**, клиенту не озвучивать.

---

## Минимум источников (адаптировать под нишу)

- qualification / scale
- pricing factors (что входит в «от»)
- catalog / scope / out-of-scope
- availability / stock / coverage / address
- scenario playbooks
- chat-only
- CRM / funnel
- notification (TG)
- hard-bans
- follow-ups-reference (**не** грузить в бота)

---

## Deliverables

A) ТЗ — [brief-template.md](references/brief-template.md)  
B) Production pack + чеклист деплоя  
C) Список регрессий из живых чатов

Нишевый скилл (Ein-Stein и т.п.) **не заменять** этим мастером: мастер его **аудирует и расширяет**.
