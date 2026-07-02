#!/usr/bin/env python3
"""Check discuss.pytorch.kr/c/news/14 for new topics and notify via Telegram.

Runs inside GitHub Actions (see .github/workflows/pytorch-news-notify.yml).
State (already-seen topic ids) is persisted at .vault-meta/pytorch-news-seen.json
and committed back to the repo by the workflow after each run.
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

STATE_PATH = ".vault-meta/pytorch-news-seen.json"
CATEGORY_JSON_URL = "https://discuss.pytorch.kr/c/news/14.json"
CATEGORY_URL = "https://discuss.pytorch.kr/c/news/14"
MAX_ITEMS_IN_MESSAGE = 15


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "llm-wiki-news-bot/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def load_state() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"source": CATEGORY_URL, "seen_topic_ids": []}


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


def main() -> int:
    state = load_state()
    seen = set(state.get("seen_topic_ids", []))

    try:
        data = fetch_json(CATEGORY_JSON_URL)
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"Failed to fetch category JSON: {e}", file=sys.stderr)
        return 1

    topics = data.get("topic_list", {}).get("topics", [])
    if not topics:
        print("No topics found in response; leaving state untouched.", file=sys.stderr)
        return 1

    new_items = []
    for t in topics:
        tid = t.get("id")
        if tid is None or tid in seen:
            continue
        slug = t.get("slug", "")
        new_items.append(
            {
                "id": tid,
                "title": t.get("title", "(제목 없음)"),
                "url": f"https://discuss.pytorch.kr/t/{slug}/{tid}",
            }
        )

    if new_items:
        lines = [f"\U0001F4F0 PyTorchKR 새 글 {len(new_items)}건"]
        for item in new_items[:MAX_ITEMS_IN_MESSAGE]:
            lines.append(f"- {item['title']}\n  {item['url']}")
        if len(new_items) > MAX_ITEMS_IN_MESSAGE:
            lines.append(f"...외 {len(new_items) - MAX_ITEMS_IN_MESSAGE}건 더")
        send_telegram("\n".join(lines))
        print(f"Sent notification for {len(new_items)} new topic(s).")
    else:
        print("No new topics.")

    for t in topics:
        tid = t.get("id")
        if tid is not None:
            seen.add(tid)
    state["seen_topic_ids"] = sorted(seen)
    state["last_checked"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_state(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
