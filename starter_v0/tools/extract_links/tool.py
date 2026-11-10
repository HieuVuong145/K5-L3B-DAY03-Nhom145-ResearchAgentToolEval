from __future__ import annotations

import re
from typing import Any

from tools._shared import domain, err

# http(s) URLs, stopping at whitespace and characters that usually wrap a link in prose/markdown.
_URL_RE = re.compile(r"https?://[^\s<>\"'()\[\]{}]+", re.IGNORECASE)
# Sentence punctuation that often sticks to the end of a pasted link.
_TRAILING = ".,;:!?…"


def extract_links(text: str = "", limit: int = 20) -> dict[str, Any]:
    """Pull unique http(s) links out of user-pasted text, in order of first appearance.

    Pure local tool: no network. Bad input from the model returns an error dict instead of raising.
    """
    try:
        if not isinstance(text, str):
            raise TypeError(f"text must be a string, got {type(text).__name__}")
        if not text.strip():
            raise ValueError("text is empty: pass the message or document that contains the links")
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValueError(f"limit must be an integer, got {limit!r}") from None
        if limit < 1:
            raise ValueError(f"limit must be >= 1, got {limit}")

        seen: set[str] = set()
        items: list[dict[str, str]] = []
        for match in _URL_RE.finditer(text):
            url = match.group(0).rstrip(_TRAILING)
            key = url.rstrip("/").lower()
            if key in seen:
                continue
            seen.add(key)
            items.append({"url": url, "source": domain(url)})

        return {
            "tool": "extract_links",
            "items": items[:limit],
            "total_found": len(items),
            "truncated": len(items) > limit,
        }
    except Exception as exc:
        return err("extract_links", exc)
