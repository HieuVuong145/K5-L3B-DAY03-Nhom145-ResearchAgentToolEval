---
name: extract_links
track: core
kind: local_formatter
requires_env: []
inputs: [text, limit]
outputs: [items, total_found, truncated]
side_effect: false
---
# extract_links

Pulls the unique `http(s)` links out of text the user pasted (a newsletter, a chat message, a list of
sources) and returns each with its domain, in order of first appearance. No network call.

Typical flow: user pastes a block of text → `extract_links` → `fetch` on the link(s) the user wants read.

Behaviour:
- Trailing sentence punctuation (`.`, `,`, `;`, `:`, `!`, `?`, `…`) and wrapping brackets/quotes are not part of the URL.
- Duplicates are removed, ignoring case and a trailing `/`.
- `limit` caps the returned items; `total_found` and `truncated` say how many there were.
- Empty or non-string `text`, or `limit < 1`, returns an error dict (`error`, `message`) instead of raising.
