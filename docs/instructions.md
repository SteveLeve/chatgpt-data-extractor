# Instructions

The `./source-data` directory contains a ChatGPT bulk export. These files are hard to read directly; the goal is to extract each conversation into a readable Markdown transcript with a YAML header and place any related artifacts alongside it.

This document defines inputs, expected outputs, extraction rules, and acceptance criteria.

> [!IMPORTANT]
> **For Developers & Agents:**
> Please refer to [docs/AGENTS.md](docs/AGENTS.md) for development guidelines, documentation standards (ADRs, Specs, Journal), and the project vision.
> **Always document your intent before beginning code changes.**

## Inputs

- `source-data/conversations.json` (preferred): Array of conversation objects with a `mapping` of message nodes.
- `source-data/chat.html` (fallback): HTML file embedding the same JSON as `var jsonData = [...]`.
- Optional metadata:
  - `source-data/shared_conversations.json`: Share info by `conversation_id` (may not match if top-level IDs are missing).
  - `source-data/message_feedback.json`: List of message ratings/feedback (empty in current export).
  - `source-data/user.json`: Export owner metadata.
  - `source-data/dalle-generations/*.webp`: Generated images without an obvious mapping file.

Notes observed in this export:
- Conversations in `conversations.json` do not show an explicit top-level `id` field; messages are reachable via the `mapping` graph.
- Messages can include `metadata.attachments` entries that may not exist on disk in this export; record them even if the files are missing.
- No explicit “project/workspace” grouping was found in the data.

## Outputs

Create one folder per conversation under `./conversations`:

- Folder name: `<YYYYMMDD-HHMMSS>_<slug-title>[_<short-stable-id>]`
  - `YYYYMMDD-HHMMSS` comes from conversation create time (UTC).
  - `slug-title` is a filesystem-safe version of `title` (lowercase, spaces→`-`, strip unsafe chars, collapse dashes).
  - `short-stable-id` is optional; recommended when titles collide. See “Stable ID”.

Inside each folder:
- `conversation.md` containing YAML front matter + Markdown transcript.
- `attachments/` (optional) containing any copied referenced files that exist locally.
- `artifacts/` (optional) for additional items you can confidently associate with the conversation.

## YAML Front Matter Schema

Include, when available:
- `title`: Conversation title.
- `created_at`: ISO 8601 UTC timestamp of conversation creation.
- `updated_at`: ISO 8601 UTC timestamp (max of message times if missing).
- `stable_id`: Short stable ID for the conversation (see below).
- `source`: `conversations.json` or `chat.html`.
- `message_count`: Number of included messages.
- `participants`: Unique set of roles encountered (e.g., `[user, assistant]`).
- `shared`: Boolean if matched via `shared_conversations.json`.
- `share_id`: If matched via `shared_conversations.json`.
- `attachments`: List of attachment metadata discovered in messages (id, name, mimeType, present: true/false, path if copied).
- `owner_email`: From `user.json`, if present.

Keep the header minimal but consistent; omit keys that are unknown.

## Stable ID

Because some exports omit a top-level conversation `id`, derive a stable identifier as:
- Collect all node IDs from `mapping` where `message` is non-null.
- Sort them lexicographically, join with `\n`, compute SHA-1, and record the first 10 hex chars as `stable_id`.
- Use this only to disambiguate folders or as metadata; do not depend on it being globally unique across different exports.

## Transcript Formatting (Markdown Body)

- One section per message in chronological order, oldest to newest.
- For each message:
  - Header line: `## [<role>] <timestamp>`
    - `role` from `message.author.role` (e.g., user, assistant, system, tool).
    - `timestamp` is ISO 8601 UTC from `message.create_time` if present; otherwise omit.
  - Content:
    - For `content.content_type == "text"`: join `content.parts` with double newlines.
    - For `content.content_type == "tether_quote"`: render as a blockquote.
    - For other content types: include a fenced code block labeled with the type and JSON payload for now.
- Preserve code fences that appear inside message text.

### Message Inclusion Rules

- Exclude messages that are visually hidden: `message.metadata.is_visually_hidden_from_conversation == true`.
- Exclude empty system placeholders with no visible content.
- Include `tool` messages only if they carry meaningful user-visible content; otherwise omit by default.
- If multiple children/branches exist, order by `message.create_time` ascending across all nodes to produce a linear transcript. If `create_time` is absent, fall back to `update_time`, then lexical `id`.

Rationale: Not all exports include a `current_node` pointer; ordering by time yields a sensible single-path transcript even when branches exist.

## Attachments and Artifacts

- For each message, if `message.metadata.attachments` exists, record the list in YAML under `attachments`.
- If a referenced attachment file exists in the export, copy it into `attachments/` and record the relative path.
- If the file is not present in the export, record `present: false` and skip copying.
- DALL·E images: without a mapping JSON, do not guess associations. If a message text explicitly references a known filename in `source-data/dalle-generations/`, copy it into `artifacts/` and link to it. Otherwise, ignore global images.

## Projects/Workspaces

If the export includes an explicit project/workspace identifier at the conversation level (examples: `project`, `project_id`, `workspace_id`, `team_id`), insert one additional folder level per project under `./conversations/<project>/...` using a slugified project name or the ID. If no such identifier exists (as in this export), place conversations directly under `./conversations`.

## Fallback to chat.html

If `conversations.json` is missing or invalid:
- Parse `source-data/chat.html` and extract the JSON array from the `var jsonData = ...` assignment.
- Decode HTML entities inside message content.
- Apply the same processing rules as above.

## Script Requirements

- Language: Python 3.10+ (standard library only; `argparse`, `json`, `hashlib`, `datetime`, `pathlib`, `html` suggested).
- CLI usage example:
  - `python scripts/export_conversations.py --input source-data --output conversations --prefer json`
- CLI options:
  - `--input`: Path to `source-data` directory (default: `source-data`).
  - `--output`: Destination root (default: `conversations`).
  - `--prefer`: `json` or `html` (default: `json`).
  - `--include-tools`: Include tool messages (default: false).
  - `--copy-attachments`: Copy available attachments (default: true).
  - `--dry-run`: Write nothing; print planned actions (default: false).

## Acceptance Criteria

- Each conversation becomes one folder with a `conversation.md`.
- YAML front matter includes `title`, `created_at`, `updated_at`, `stable_id`, `source`, and `message_count` when available.
- Messages appear in chronological order with clear role labeling.
- Hidden/system placeholder messages are excluded; visible content is preserved.
- Any referenced attachments that exist are copied and listed with relative paths; missing ones are still recorded in YAML with `present: false`.
- The script runs on the provided export without extra dependencies and produces deterministic folder names for the same input.

## Edge Cases

- Missing timestamps: Use available fields, or omit the timestamp for that message.
- Duplicate titles at the same timestamp: append `_a`, `_b` or include `_<short-stable-id>` to avoid collisions.
- Extremely long titles: truncate `slug-title` to 80 characters.
- Non-ASCII in titles/content: allow in content; normalize to ASCII for slugs.

---

Implementation tip: start by writing a loader that returns a normalized in-memory structure `[Conversation] -> [Message]` independent of whether the source is JSON or HTML. Keep ordering and filtering logic in a single place so both sources behave identically.
