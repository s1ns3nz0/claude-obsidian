#!/usr/bin/env python3
"""Poll Telegram for incoming commands and reply with the current PyTorchKR
news list on demand.

This is the "pull" counterpart to pytorch-news-notify.py (which "pushes" only
when new topics appear). Runs on a frequent cron
(.github/workflows/pytorch-news-bot-poll.yml) since Telegram's simple long
polling (getUpdates) requires periodic checking rather than a live webhook.

Commands recognized (case-insensitive, from the configured chat only):
  /news, /list, 목록, 뉴스  -> reply with the current top posts in the category
  /help, /start            -> reply with a short usage hint
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

OFFSET_STATE_PATH = ".vault-meta/telegram-update-offset.json"
CATEGORY_JSON_URL = "https://discuss.pytorch.kr/c/news/14.json"
MAX_ITEMS_IN_MESSAGE = 20

LIST_TRIGGERS = {"/news", "/list", "목록", "뉴스", "/news@llmwiki_news_bot", "/list@llmwiki_news_bot"}
HELP_TRIGGERS = {"/help", "/start", "/start@llmwiki_news_bot", "/help@llmwiki_news_bot"}

HELP_TEXT = (
    "PyTorchKR 뉴스 봇입니다.\n"
    "/news 또는 '목록' 을 보내면 현재 게시판 최신 글 목록을 보내드려요.\n"
    "새 글이 올라오면 매일 자동으로도 알려드립니다."
)


def api_call(method: str, token: str, params: dict) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_current_topics() -> list:
    req = urllib.request.Request(
        CATEGORY_JSON_URL, headers={"User-Agent": "llm-wiki-news-bot/1.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    return data.get("topic_list", {}).get("topics", [])


def format_list(topics: list) -> str:
    lines = ["\U0001F4F0 PyTorchKR 최신 글 목록"]
    for i, t in enumerate(topics[:MAX_ITEMS_IN_MESSAGE], start=1):
        title = t.get("title", "(제목 없음)")
        slug = t.get("slug", "")
        tid = t.get("id")
        lines.append(f"{i}. {title}\n   https://discuss.pytorch.kr/t/{slug}/{tid}")
    return "\n".join(lines)


def load_offset() -> int:
    try:
        with open(OFFSET_STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("offset", 0)
    except FileNotFoundError:
        return 0


def save_offset(offset: int) -> None:
    with open(OFFSET_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump({"offset": offset}, f)
        f.write("\n")


def main() -> int:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    allowed_chat_id = os.environ["TELEGRAM_CHAT_ID"]

    offset = load_offset()
    try:
        updates = api_call(
            "getUpdates", token, {"offset": offset, "timeout": 0}
        )
    except urllib.error.URLError as e:
        print(f"getUpdates failed: {e}")
        return 1

    results = updates.get("result", [])
    if not results:
        print("No new updates.")
        return 0

    max_update_id = offset - 1
    topics_cache = None

    for update in results:
        max_update_id = max(max_update_id, update.get("update_id", max_update_id))
        message = update.get("message") or update.get("edited_message")
        if not message:
            continue

        chat_id = str(message.get("chat", {}).get("id", ""))
        text = (message.get("text") or "").strip()
        text_lower = text.lower()

        if chat_id != str(allowed_chat_id):
            # Ignore messages from anyone other than the configured owner chat.
            continue

        if text_lower in LIST_TRIGGERS:
            if topics_cache is None:
                topics_cache = fetch_current_topics()
            if topics_cache:
                api_call("sendMessage", token, {"chat_id": chat_id, "text": format_list(topics_cache)})
            else:
                api_call("sendMessage", token, {"chat_id": chat_id, "text": "지금 목록을 가져오지 못했어요. 잠시 후 다시 시도해주세요."})
        elif text_lower in HELP_TRIGGERS:
            api_call("sendMessage", token, {"chat_id": chat_id, "text": HELP_TEXT})

    save_offset(max_update_id + 1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
