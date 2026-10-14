"""Day 10 SSRF defense exercise: URL policy only, ZERO network requests."""
from urllib.parse import urlsplit
from dataclasses import dataclass

ALLOWED_HOSTS=frozenset({"reports.example.test","status.example.test"})

@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str

def check_url(raw: str) -> Decision:
    if not isinstance(raw,str) or not raw or len(raw)>2048:
        return Decision(False,"invalid URL input")
    # Explicitly reject ambiguity before parsing.
    if "\\" in raw or any(ch.isspace() or ord(ch)<32 or ord(ch)==127 for ch in raw):
        return Decision(False,"backslash/whitespace/control character not allowed")
    try:
        url=urlsplit(raw)
        port=url.port  # can raise ValueError on invalid port
    except ValueError:
        return Decision(False,"malformed URL")
    if url.scheme!="https":
        return Decision(False,"only https is allowed")
    if not url.netloc or not url.hostname:
        return Decision(False,"missing hostname")
    if url.username is not None or url.password is not None:
        return Decision(False,"userinfo is forbidden")
    if url.fragment:
        return Decision(False,"fragments forbidden")
    if port not in (None,443):
        return Decision(False,"port not allowed")
    if url.hostname not in ALLOWED_HOSTS:
        return Decision(False,"host is not allowlisted")
    return Decision(True,"URL syntax matches narrow allowlist; NOT proof of safe DNS resolution")

if __name__=="__main__":
    examples=[
        "https://reports.example.test/daily",
        "https://status.example.test:443/health",
        "http://reports.example.test/daily",
        "https://reports.example.test.evil.test/",
        "https://reader@reports.example.test/",
        "https://127.0.0.1/",
        "https://reports.example.test:8080/",
        "https://reports.example.test./",
    ]
    for item in examples:
        print(f"{str(check_url(item).allowed):5} {item} -> {check_url(item).reason}")
    print("NO HTTP request is made by this script.")
