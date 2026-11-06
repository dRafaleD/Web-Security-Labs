"""Offline CSRF validation example; no HTTP server or networking."""
from dataclasses import dataclass
import hmac

TRUSTED_ORIGIN = "https://app.example.test"
SESSION_TOKEN = "server-generated-demo-token"

@dataclass(frozen=True)
class Request:
    method: str
    origin: str | None
    csrf_token: str | None

def authorize_state_change(req: Request) -> bool:
    if req.method != "POST":
        return False
    if req.origin != TRUSTED_ORIGIN:
        return False
    if req.csrf_token is None:
        return False
    return hmac.compare_digest(req.csrf_token, SESSION_TOKEN)

cases = [
    ("valid", Request("POST", TRUSTED_ORIGIN, SESSION_TOKEN), True),
    ("wrong origin", Request("POST", "https://other.example.test", SESSION_TOKEN), False),
    ("missing origin", Request("POST", None, SESSION_TOKEN), False),
    ("wrong token", Request("POST", TRUSTED_ORIGIN, "guessed"), False),
    ("missing token", Request("POST", TRUSTED_ORIGIN, None), False),
    ("wrong method", Request("GET", TRUSTED_ORIGIN, SESSION_TOKEN), False),
]
for label, req, expected in cases:
    result = authorize_state_change(req)
    print(f"{label}: {'accepted' if result else 'rejected'}")
    assert result == expected
print("All synthetic tests passed.")
