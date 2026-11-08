"""Offline webhook integrity and replay checks. All keys and events are synthetic."""
import hashlib
import hmac

DEMO_KEY = b"example-only-not-a-production-key"
MAX_SKEW_SECONDS = 300

def sign(timestamp: int, raw_body: bytes) -> str:
    message = str(timestamp).encode("ascii") + b"." + raw_body
    return hmac.new(DEMO_KEY, message, hashlib.sha256).hexdigest()

def verify(timestamp: int, raw_body: bytes, supplied_mac: str,
           now: int, seen: set[tuple[int, str]]) -> bool:
    if not isinstance(timestamp, int) or abs(now - timestamp) > MAX_SKEW_SECONDS:
        return False
    expected = sign(timestamp, raw_body)
    if not hmac.compare_digest(expected, supplied_mac):
        return False
    identity = (timestamp, expected)
    if identity in seen:
        return False
    seen.add(identity)
    return True

body = b'{"event_id":"evt-training-1","status":"ok"}'
time_sent = 1000
mac = sign(time_sent, body)
store: set[tuple[int, str]] = set()

assert verify(time_sent, body, mac, 1001, store)
assert not verify(time_sent, body, mac, 1002, store)  # Replay
assert not verify(time_sent, body + b" ", mac, 1002, set())  # One changed byte
assert not verify(time_sent, body, mac, 1301, set())  # Expired
assert not verify(time_sent, body, "0" * 64, 1001, set())  # Fake signature

print("5/5 synthetic webhook checks passed.")
print("Production requires provider-specific signing, atomic dedupe and secret rotation.")
