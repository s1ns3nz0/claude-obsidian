#!/usr/bin/env python3
"""Check discuss.pytorch.kr/c/news/14 and news.hada.io (GeekNews) for new posts,
notify via Telegram.

Runs inside GitHub Actions (see .github/workflows/pytorch-news-notify.yml).
State (already-seen topic ids per source) is persisted at
.vault-meta/pytorch-news-seen.json and committed back to the repo by the
workflow after each run.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

STATE_PATH = ".vault-meta/pytorch-news-seen.json"
PYTORCH_CATEGORY_JSON_URL = "https://discuss.pytorch.kr/c/news/14.json"
GEEKNEWS_RSS_URL = "https://news.hada.io/rss/news"
MAX_ITEMS_IN_MESSAGE = 15
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "llm-wiki-news-bot/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "llm-wiki-news-bot/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8")


def load_state() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


def send_telegram(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        print(
            f"Missing secret(s): TELEGRAM_BOT_TOKEN set={bool(token)}, "
            f"TELEGRAM_CHAT_ID set={bool(chat_id)}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Telegram API error {e.code}: {body}", file=sys.stderr)
        raise


def fetch_pytorch_topics() -> list:
    data = fetch_json(PYTORCH_CATEGORY_JSON_URL)
    topics = data.get("topic_list", {}).get("topics", [])
    items = []
    for t in topics:
        tid = t.get("id")
        if tid is None:
            continue
        slug = t.get("slug", "")
        items.append(
            {
                "id": str(tid),
                "title": t.get("title", "(제목 없음)"),
                "url": f"https://discuss.pytorch.kr/t/{slug}/{tid}",
            }
        )
    return items


def fetch_geeknews_topics() -> list:
    root = ET.fromstring(fetch_text(GEEKNEWS_RSS_URL))
    items = []
    for entry in root.findall("atom:entry", ATOM_NS):
        link_el = entry.find("atom:link", ATOM_NS)
        href = link_el.get("href") if link_el is not None else None
        if not href:
            continue
        tid = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("id", [None])[0]
        if tid is None:
            continue
        title_el = entry.find("atom:title", ATOM_NS)
        items.append(
            {
                "id": tid,
                "title": title_el.text if title_el is not None else "(제목 없음)",
                "url": href,
            }
        )
    return items


def try_fetch(label: str, fetch_fn) -> list | None:
    try:
        items = fetch_fn()
    except (urllib.error.URLError, json.JSONDecodeError, ET.ParseError) as e:
        print(f"Failed to fetch {label}: {e}", file=sys.stderr)
        return None
    if not items:
        print(f"No topics found for {label}; leaving state untouched.", file=sys.stderr)
        return None
    return items


def format_section(label: str, new_items: list) -> list:
    lines = [f"\U0001F4F0 {label} 새 글 {len(new_items)}건"]
    for item in new_items[:MAX_ITEMS_IN_MESSAGE]:
        lines.append(f"- {item['title']}\n  {item['url']}")
    if len(new_items) > MAX_ITEMS_IN_MESSAGE:
        lines.append(f"...외 {len(new_items) - MAX_ITEMS_IN_MESSAGE}건 더")
    return lines


def main() -> int:
    state = load_state()
    pytorch_seen = set(state.get("seen_topic_ids", []))
    geeknews_seen = set(state.get("geeknews_seen_topic_ids", []))

    pytorch_topics = try_fetch("PyTorchKR", fetch_pytorch_topics)
    geeknews_topics = try_fetch("GeekNews", fetch_geeknews_topics)

    if pytorch_topics is None and geeknews_topics is None:
        return 1

    message_sections = []

    if pytorch_topics is not None:
        new_items = [t for t in pytorch_topics if t["id"] not in pytorch_seen]
        if new_items:
            message_sections.extend(format_section("PyTorchKR", new_items))
        pytorch_seen.update(t["id"] for t in pytorch_topics)

    if geeknews_topics is not None:
        new_items = [t for t in geeknews_topics if t["id"] not in geeknews_seen]
        if new_items:
            if message_sections:
                message_sections.append("")
            message_sections.extend(format_section("GeekNews", new_items))
        geeknews_seen.update(t["id"] for t in geeknews_topics)

    if message_sections:
        send_telegram("\n".join(message_sections))
        print("Sent notification.")
    else:
        print("No new topics.")

    state["seen_topic_ids"] = sorted(pytorch_seen)
    state["geeknews_seen_topic_ids"] = sorted(geeknews_seen)
    state["last_checked"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_state(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
