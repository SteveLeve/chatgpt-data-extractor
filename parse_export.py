import argparse
import datetime as dt
import hashlib
import html as html_mod
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _read_json(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def _extract_json_from_html(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding='utf-8', errors='replace')
    # Greedy capture of the JSON array assigned to var jsonData = ...;
    m = re.search(r"var\s+jsonData\s*=\s*(\[.*?\])\s*;", text, flags=re.DOTALL)
    if not m:
        raise ValueError("jsonData array not found in chat.html")
    json_blob = m.group(1)
    # Unescape HTML entities that may appear inside strings
    json_blob = html_mod.unescape(json_blob)
    return json.loads(json_blob)


def _ts_to_iso(ts: Optional[float]) -> Optional[str]:
    if ts is None:
        return None
    try:
        return dt.datetime.fromtimestamp(float(ts), tz=dt.timezone.utc).isoformat()
    except Exception:
        return None


def _iso_to_stamp_for_slug(iso_ts: Optional[str]) -> str:
    if not iso_ts:
        return "00000000-000000"
    try:
        d = dt.datetime.fromisoformat(iso_ts.replace('Z', '+00:00')).astimezone(dt.timezone.utc)
        return d.strftime('%Y%m%d-%H%M%S')
    except Exception:
        return "00000000-000000"


def _slugify(text: str, max_len: int = 80) -> str:
    if not text:
        return "untitled"
    # Normalize to ASCII
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    # Replace spaces with dashes, remove unsafe chars
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9\-]", "", text)
    text = re.sub(r"-+", "-", text).strip('-')
    if not text:
        text = "untitled"
    return text[:max_len]


def _compute_stable_id(conversation: Dict[str, Any]) -> str:
    mapping = conversation.get('mapping', {}) or {}
    node_ids = [nid for nid, node in mapping.items() if (node or {}).get('message')]
    node_ids.sort()
    h = hashlib.sha1('\n'.join(node_ids).encode('utf-8')).hexdigest()
    return h[:10]


def _collect_messages(conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = conversation.get('mapping', {}) or {}
    messages: List[Dict[str, Any]] = []
    for node in mapping.values():
        msg = (node or {}).get('message')
        if msg:
            messages.append(msg)
    # Order: create_time asc, then update_time, then id
    def key_fn(m: Dict[str, Any]):
        ct = m.get('create_time')
        ut = m.get('update_time')
        mid = m.get('id') or ''
        return (
            float(ct) if isinstance(ct, (int, float, str)) and str(ct).replace('.', '', 1).isdigit() else float('inf'),
            float(ut) if isinstance(ut, (int, float, str)) and str(ut).replace('.', '', 1).isdigit() else float('inf'),
            mid,
        )
    messages.sort(key=key_fn)
    return messages


def _is_hidden(msg: Dict[str, Any]) -> bool:
    meta = (msg.get('metadata') or {})
    if meta.get('is_visually_hidden_from_conversation') is True:
        return True
    # Hide empty system placeholders
    role = (msg.get('author') or {}).get('role')
    content = msg.get('content') or {}
    ctype = content.get('content_type')
    parts = content.get('parts') or []
    if role == 'system' and (ctype == 'text') and all((p or '').strip() == '' for p in parts):
        return True
    return False


def _render_message_content(msg: Dict[str, Any]) -> Tuple[str, str]:
    content = msg.get('content') or {}
    ctype = content.get('content_type') or 'text'
    if ctype == 'text':
        parts = content.get('parts') or []
        text = '\n\n'.join(str(p) for p in parts if p is not None)
        return ctype, text
    elif ctype == 'tether_quote':
        text = content.get('text') or ''
        # Render as blockquote
        quoted = '\n'.join(
            '> ' + line if line.strip() else '>' for line in str(text).splitlines()
        )
        return ctype, quoted
    else:
        # Fallback: include JSON payload
        payload = json.dumps(content, ensure_ascii=False, indent=2)
        return ctype, f"```{ctype}\n{payload}\n```"


def _gather_attachments(conversation: Dict[str, Any]) -> List[Dict[str, Any]]:
    attachments: List[Dict[str, Any]] = []
    for msg in _collect_messages(conversation):
        meta = (msg.get('metadata') or {})
        att = meta.get('attachments') or []
        for a in att:
            attachments.append({
                'id': a.get('id'),
                'name': a.get('name'),
                'mimeType': a.get('mimeType'),
                'present': False,
                'path': None,
            })
    return attachments


def load_conversations(input_dir: Path, prefer: str) -> Tuple[List[Dict[str, Any]], str]:
    json_path = input_dir / 'conversations.json'
    html_path = input_dir / 'chat.html'
    if prefer == 'json' and json_path.exists():
        return _read_json(json_path), 'conversations.json'
    if prefer == 'html' and html_path.exists():
        return _extract_json_from_html(html_path), 'chat.html'
    # Fallback to whichever exists
    if json_path.exists():
        return _read_json(json_path), 'conversations.json'
    if html_path.exists():
        return _extract_json_from_html(html_path), 'chat.html'
    raise FileNotFoundError('Neither conversations.json nor chat.html found')


def load_owner_email(input_dir: Path) -> Optional[str]:
    p = input_dir / 'user.json'
    if not p.exists():
        return None
    try:
        data = _read_json(p)
        return data.get('email')
    except Exception:
        return None


def load_shared_index(input_dir: Path) -> Dict[str, Dict[str, Any]]:
    p = input_dir / 'shared_conversations.json'
    if not p.exists():
        return {}
    try:
        items = _read_json(p)
        return {item.get('conversation_id'): item for item in items if item.get('conversation_id')}
    except Exception:
        return {}


def write_conversation_folder(
    conversation: Dict[str, Any],
    conv_index: int,
    source_label: str,
    output_root: Path,
    owner_email: Optional[str],
    shared_index: Dict[str, Dict[str, Any]],
    include_tools: bool,
    copy_attachments: bool,
    dry_run: bool,
) -> None:
    title = conversation.get('title') or f'Conversation {conv_index + 1}'
    messages = _collect_messages(conversation)
    # Filter hidden and tool messages as configured
    filtered: List[Dict[str, Any]] = []
    for m in messages:
        if _is_hidden(m):
            continue
        role = (m.get('author') or {}).get('role')
        if role == 'tool' and not include_tools:
            continue
        filtered.append(m)

    # Participants
    participants = sorted({(m.get('author') or {}).get('role') or 'unknown' for m in filtered})

    # Times
    created_at_iso = _ts_to_iso(conversation.get('create_time'))
    # If update_time missing on conversation, compute from messages
    conv_update_ts = conversation.get('update_time')
    if conv_update_ts is None:
        max_ts = None
        for m in filtered:
            ct = m.get('create_time')
            if isinstance(ct, (int, float)):
                max_ts = max(ct, max_ts or ct)
        conv_update_iso = _ts_to_iso(max_ts)
    else:
        conv_update_iso = _ts_to_iso(conv_update_ts)

    stable_id = _compute_stable_id(conversation)
    stamp = _iso_to_stamp_for_slug(created_at_iso)
    slug = _slugify(title)
    # Optional project/workspace grouping
    project_key = conversation.get('project') or conversation.get('project_id') or conversation.get('workspace_id') or conversation.get('team_id')
    project_root = output_root
    if project_key:
        project_slug = _slugify(str(project_key))
        project_root = output_root / project_slug

    folder_name = f"{stamp}_{slug}"
    folder_path = project_root / folder_name
    if folder_path.exists():
        folder_name = f"{folder_name}_{stable_id[:8]}"
        folder_path = project_root / folder_name

    # YAML front matter
    attachments = _gather_attachments(conversation)
    # Shared info: only if conversation has an id that matches index (rare in this export)
    conv_id = conversation.get('id')
    shared_entry = shared_index.get(conv_id) if conv_id else None

    yaml_lines: List[str] = ["---"]
    def add_yaml(k: str, v: Any):
        if v is None:
            return
        if isinstance(v, bool):
            yaml_lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            yaml_lines.append(f"{k}: {v}")
        elif isinstance(v, list):
            yaml_lines.append(f"{k}:")
            for item in v:
                if isinstance(item, dict):
                    yaml_lines.append("  -")
                    for dk, dv in item.items():
                        if dv is None:
                            continue
                        yaml_lines.append(f"    {dk}: {json.dumps(dv, ensure_ascii=False)}")
                else:
                    yaml_lines.append(f"  - {json.dumps(item, ensure_ascii=False)}")
        else:
            yaml_lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")

    add_yaml('title', title)
    add_yaml('created_at', created_at_iso)
    add_yaml('updated_at', conv_update_iso)
    add_yaml('stable_id', stable_id)
    add_yaml('source', source_label)
    add_yaml('message_count', len(filtered))
    add_yaml('participants', participants)
    if project_key:
        add_yaml('project', str(project_key))
    add_yaml('shared', bool(shared_entry) if shared_entry is not None else None)
    if shared_entry:
        add_yaml('share_id', shared_entry.get('id'))
    add_yaml('owner_email', owner_email)
    # Mark attachments presence (copying handled later)
    add_yaml('attachments', attachments if attachments else None)
    yaml_lines.append("---\n")

    # Build body
    body_lines: List[str] = []
    for m in filtered:
        role = (m.get('author') or {}).get('role') or 'unknown'
        ts_iso = _ts_to_iso(m.get('create_time'))
        header = f"## [{role}] {ts_iso}" if ts_iso else f"## [{role}]"
        body_lines.append(header)
        ctype, text = _render_message_content(m)
        if text:
            body_lines.append("")
            body_lines.append(text)
            body_lines.append("")

    # Planned actions
    md_rel = Path(folder_name) / 'conversation.md'
    if dry_run:
        print(f"[DRY-RUN] Would write: {md_rel}")
    else:
        folder_path.mkdir(parents=True, exist_ok=True)
        # Attempt to copy attachments if we ever find actual files (none mapped in this export)
        if copy_attachments and any(a.get('present') for a in attachments):
            (folder_path / 'attachments').mkdir(exist_ok=True)
        with (folder_path / 'conversation.md').open('w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(yaml_lines))
            f.write('\n'.join(body_lines).rstrip() + '\n')


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description='Extract ChatGPT export into Markdown conversations.')
    parser.add_argument('--input', default='source-data', help='Path to source-data directory')
    parser.add_argument('--output', default='conversations', help='Destination root directory')
    parser.add_argument('--prefer', choices=['json', 'html'], default='json', help='Preferred input format')
    parser.add_argument('--include-tools', action='store_true', help='Include tool messages')
    parser.add_argument('--copy-attachments', dest='copy_attachments', action='store_true', default=True, help='Copy available attachments')
    parser.add_argument('--no-copy-attachments', dest='copy_attachments', action='store_false', help='Do not copy attachments')
    parser.add_argument('--dry-run', action='store_true', help='Do not write files; print planned actions')
    args = parser.parse_args(argv)

    input_dir = Path(args.input)
    output_root = Path(args.output)
    try:
        conversations, source_label = load_conversations(input_dir, args.prefer)
    except Exception as e:
        print(f"Error loading export: {e}")
        return 2

    owner_email = load_owner_email(input_dir)
    shared_index = load_shared_index(input_dir)

    if not args.dry_run:
        output_root.mkdir(parents=True, exist_ok=True)

    for i, conv in enumerate(conversations):
        write_conversation_folder(
            conversation=conv,
            conv_index=i,
            source_label=source_label,
            output_root=output_root,
            owner_email=owner_email,
            shared_index=shared_index,
            include_tools=args.include_tools,
            copy_attachments=args.copy_attachments,
            dry_run=args.dry_run,
        )

    print(f"Processed {len(conversations)} conversation(s) from {source_label}.")
    print(f"Output root: {output_root}")
    if args.dry_run:
        print("No files were written (dry run).")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
