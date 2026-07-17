#!/usr/bin/env python3
"""test_pytorch_news_notify.py — hermetic tests for scripts/pytorch-news-notify.py.

Covers chunk_message() packing/limit/order guarantees and send_telegram()'s
429 retry-with-backoff path. No real network calls (urlopen is mocked).

Usage:
  python3 tests/test_pytorch_news_notify.py
"""
import importlib.util
import io
import json
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
HELPER = ROOT / "scripts" / "pytorch-news-notify.py"

spec = importlib.util.spec_from_file_location("pytorch_news_notify", HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Fail(SystemExit):
    pass


def assert_eq(label, expected, actual):
    if expected != actual:
        raise Fail(f"FAIL {label}: expected {expected!r}, got {actual!r}")
    print(f"OK   {label}")


def assert_true(label, cond, hint=""):
    if not cond:
        raise Fail(f"FAIL {label}{(': ' + hint) if hint else ''}")
    print(f"OK   {label}")


# ─── chunk_message: empty input ───────────────────────────────────────────────
def test_chunk_message_empty():
    assert_eq("empty lines → no chunks", [], m.chunk_message([]))


# ─── chunk_message: everything fits in one chunk ──────────────────────────────
def test_chunk_message_single_chunk():
    lines = [f"- item {i}" for i in range(5)]
    chunks = m.chunk_message(lines, limit=1000)
    assert_eq("small input → 1 chunk", 1, len(chunks))
    assert_true("all lines present", all(f"item {i}" in chunks[0] for i in range(5)))


# ─── chunk_message: packs many items across multiple chunks, none dropped ────
def test_chunk_message_packs_without_dropping():
    lines = [f"- title {i} " + ("x" * 100) for i in range(50)]
    chunks = m.chunk_message(lines, limit=m.TELEGRAM_MESSAGE_LIMIT)
    assert_true("more than one chunk for 50 long lines", len(chunks) > 1)
    for c in chunks:
        assert_true(f"chunk len {len(c)} <= limit", len(c) <= m.TELEGRAM_MESSAGE_LIMIT)
    total_items = sum(c.count("- title") for c in chunks)
    assert_eq("no items dropped", 50, total_items)
    # order preserved: item 0 appears before item 49 across the joined chunks
    joined = "\n".join(chunks)
    assert_true("order preserved", joined.index("title 0 ") < joined.index("title 49 "))


# ─── chunk_message: a single line longer than the limit is bounded, not left oversized
def test_chunk_message_oversized_single_line():
    huge_line = "- " + ("x" * (m.TELEGRAM_MESSAGE_LIMIT + 500))
    chunks = m.chunk_message([huge_line], limit=m.TELEGRAM_MESSAGE_LIMIT)
    assert_eq("oversized line → 1 chunk", 1, len(chunks))
    assert_true("chunk bounded to limit", len(chunks[0]) <= m.TELEGRAM_MESSAGE_LIMIT)
    assert_true("truncation marker present", chunks[0].endswith("…"))


# ─── chunk_message: an oversized line mixed with normal lines doesn't blow the
#     following chunk's budget ──────────────────────────────────────────────
def test_chunk_message_oversized_line_mixed_with_normal_lines():
    huge_line = "x" * (m.TELEGRAM_MESSAGE_LIMIT + 500)
    lines = [huge_line, "- normal item"]
    chunks = m.chunk_message(lines, limit=m.TELEGRAM_MESSAGE_LIMIT)
    for c in chunks:
        assert_true(f"chunk len {len(c)} <= limit", len(c) <= m.TELEGRAM_MESSAGE_LIMIT)
    assert_true("normal item preserved", any("normal item" in c for c in chunks))


# ─── send_telegram: retries once on 429 then succeeds ─────────────────────────
def test_send_telegram_retries_on_429():
    calls = {"n": 0}

    class FakeResp:
        def __enter__(self):
            return io.BytesIO(b"{}")

        def __exit__(self, *a):
            return False

    def fake_urlopen_cm(req, timeout=20):
        calls["n"] += 1
        if calls["n"] == 1:
            body = io.BytesIO(json.dumps({"parameters": {"retry_after": 0}}).encode())
            raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, body)
        return FakeResp()

    with mock.patch.object(m.os, "environ", {"TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}), \
         mock.patch.object(m.time, "sleep", lambda s: None), \
         mock.patch.object(m.urllib.request, "urlopen", fake_urlopen_cm):
        m.send_telegram("hello")
    assert_eq("retried exactly once before success", 2, calls["n"])


# ─── send_telegram: raises after exhausting all 429 retries ───────────────────
def test_send_telegram_raises_after_exhausting_429_retries():
    calls = {"n": 0}

    def fake_urlopen(req, timeout=20):
        calls["n"] += 1
        body = io.BytesIO(json.dumps({"parameters": {"retry_after": 0}}).encode())
        raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, body)

    with mock.patch.object(m.os, "environ", {"TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}), \
         mock.patch.object(m.time, "sleep", lambda s: None), \
         mock.patch.object(m.urllib.request, "urlopen", fake_urlopen):
        try:
            m.send_telegram("hello")
            raise Fail("FAIL expected HTTPError to propagate after exhausting retries")
        except urllib.error.HTTPError:
            pass
    assert_eq("exactly 3 attempts made", 3, calls["n"])


# ─── send_telegram: retry_after is capped so it can't blow the CI job budget ──
def test_send_telegram_caps_retry_after():
    calls = {"n": 0}
    sleeps = []

    class FakeResp:
        def __enter__(self):
            return io.BytesIO(b"{}")

        def __exit__(self, *a):
            return False

    def fake_urlopen_cm(req, timeout=20):
        calls["n"] += 1
        if calls["n"] == 1:
            body = io.BytesIO(json.dumps({"parameters": {"retry_after": 120}}).encode())
            raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, body)
        return FakeResp()

    with mock.patch.object(m.os, "environ", {"TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}), \
         mock.patch.object(m.time, "sleep", lambda s: sleeps.append(s)), \
         mock.patch.object(m.urllib.request, "urlopen", fake_urlopen_cm):
        m.send_telegram("hello")
    assert_eq("slept once", 1, len(sleeps))
    assert_true("retry_after capped well under Telegram's 120s", sleeps[0] <= 15, f"slept {sleeps[0]}s")


# ─── send_telegram: non-429 HTTP error raises immediately, no retry ───────────
def test_send_telegram_raises_on_non_429():
    calls = {"n": 0}

    def fake_urlopen(req, timeout=20):
        calls["n"] += 1
        body = io.BytesIO(b'{"description": "bad request"}')
        raise urllib.error.HTTPError(req.full_url, 400, "Bad Request", {}, body)

    with mock.patch.object(m.os, "environ", {"TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}), \
         mock.patch.object(m.urllib.request, "urlopen", fake_urlopen):
        try:
            m.send_telegram("hello")
            raise Fail("FAIL expected HTTPError to propagate")
        except urllib.error.HTTPError:
            pass
    assert_eq("no retry on non-429", 1, calls["n"])


def main():
    print("=== test_pytorch_news_notify.py ===")
    test_chunk_message_empty()
    test_chunk_message_single_chunk()
    test_chunk_message_packs_without_dropping()
    test_chunk_message_oversized_single_line()
    test_chunk_message_oversized_line_mixed_with_normal_lines()
    test_send_telegram_retries_on_429()
    test_send_telegram_raises_after_exhausting_429_retries()
    test_send_telegram_caps_retry_after()
    test_send_telegram_raises_on_non_429()
    print("\nAll pytorch-news-notify tests passed.")


if __name__ == "__main__":
    main()
