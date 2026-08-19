# -*- coding: utf-8 -*-
"""Wrap sources/*.md into suvvy-qa Direct Question format. Copy into niche skill suvvy-qa/."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
QA = Path(__file__).resolve().parent

# (qa_filename, source_filename, Exact Suvvy Title)
MAP = [
    ("01-qualification-by-scale.md", "qualification-by-scale.md", "Qualification by Scale"),
    ("02-pricing-factors.md", "pricing-factors.md", "Pricing Factors"),
    ("03-warehouse-address.md", "warehouse-address.md", "Warehouse Address"),
    ("04-availability-rules.md", "availability-rules.md", "Availability Rules"),
    ("05-notification-in-telegram.md", "notification-telegram.md", "Notification in telegram"),
    ("06-catalog-assortment.md", "catalog-assortment.md", "Catalog Assortment"),
    ("07-chat-only-mode.md", "chat-only-mode.md", "Chat Only Mode"),
    ("08-scenario-playbooks.md", "scenario-playbooks.md", "Scenario Playbooks"),
    ("10-bitrix-funnel-stage.md", "bitrix-funnel-stage.md", "Bitrix Funnel Stage"),
]


def wrap(title: str, body: str) -> str:
    body = body.strip().replace("\r\n", "\n")
    return (
        "# Suvvy Direct Question — paste into «Вопрос — ответ»\n\n"
        f"**Title (exact):** `{title}`\n\n"
        "**Answer / body:**\n\n"
        f"```\n{body}\n```\n"
    )


def main() -> None:
    for qa_name, src_name, title in MAP:
        src = SOURCES / src_name
        body = src.read_text(encoding="utf-8")
        if body.startswith("# "):
            body = body.split("\n", 1)[1].lstrip()
        (QA / qa_name).write_text(wrap(title, body), encoding="utf-8")
        print("wrapped", qa_name, "->", title)


if __name__ == "__main__":
    main()
