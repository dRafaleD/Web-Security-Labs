#!/usr/bin/env python3
"""Offline JSON syntax/size guard; no network or API endpoints."""
import json

MAX_BYTES = 256
MAX_DEPTH = 4
MAX_NODES = 20


def unique_keys(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def validate(content_type: str, body: bytes) -> tuple[bool, str]:
    media_type = content_type.split(";", 1)[0].strip().lower()
    if media_type != "application/json":
        return False, "unexpected media type"
    if len(body) > MAX_BYTES:
        return False, "raw byte limit exceeded"

    try:
        decoded = body.decode("utf-8", errors="strict")
        data = json.loads(
            decoded, object_pairs_hook=unique_keys,
            parse_constant=reject_constant
        )
    except (UnicodeDecodeError, ValueError, RecursionError) as error:
        return False, f"invalid JSON: {error}"

    # Post-parse limits: they DO NOT bound the cost of initial json.loads.
    nodes = 0
    stack = [(data, 1)]
    while stack:
        current, depth = stack.pop()
        nodes += 1
        if nodes > MAX_NODES:
            return False, "node limit exceeded"
        if depth > MAX_DEPTH:
            return False, "nesting depth exceeded"
        if isinstance(current, dict):
            stack.extend((value, depth + 1) for value in current.values())
        elif isinstance(current, list):
            stack.extend((value, depth + 1) for value in current)
    return True, "syntax and structural checks passed; no authorization implied"


def main():
    cases = [
        ("small valid object", "application/json; charset=utf-8",
         b'{"id":7,"action":"read"}', True),
        ("wrong media type", "text/plain", b'{"id":7}', False),
        ("oversized", "application/json",
         b'{"data":"' + b"A" * 300 + b'"}', False),
        ("duplicate keys", "application/json",
         b'{"role":"reader","role":"admin"}', False),
        ("invalid UTF-8", "application/json", b'{"v":"\xff"}', False),
        ("nonstandard number", "application/json", b'{"v":NaN}', False),
        ("too deep", "application/json", b'{"a":{"b":{"c":{"d":1}}}}', False),
    ]
    for label, content_type, body, expected in cases:
        allowed, reason = validate(content_type, body)
        print(f"{label:20} {'ALLOW' if allowed else 'DENY':5} | {reason}")
        assert allowed is expected, (label, reason)
    print("All synthetic checks passed.")


if __name__ == "__main__":
    main()
