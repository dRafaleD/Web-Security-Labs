"""Redact sensitive query parameters and bearer tokens from synthetic web log lines."""
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SENSITIVE = {"password", "token", "api_key", "secret"}


def redact_url(url):
    parts = urlsplit(url)
    query = [(k, "[REDACTED]" if k.lower() in SENSITIVE else v) for k, v in parse_qsl(parts.query)]
    return urlunsplit(parts._replace(query=urlencode(query, safe="[]")))


def redact_line(line):
    line = re.sub(r"(Bearer\s+)[\w.-]+", r"\1[REDACTED]", line)
    return re.sub(r"https?://\S+", lambda m: redact_url(m.group()), line)


if __name__ == "__main__":
    raw = "GET https://app.example.test/login?user=alice&password=hunter2&next=/home Authorization: Bearer abc.def-123"
    out = redact_line(raw)
    print(out)
    assert "hunter2" not in out and "abc.def-123" not in out
    assert "user=alice" in out and "next=%2Fhome" in out or "next=/home" in out
    print("PASS: sensitive parameters and bearer tokens are redacted; other fields survive.")
    print("Review: unknown field names slip through; prefer logging an allow-list of fields.")
