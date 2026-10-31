"""Enforce idle and absolute session timeouts on the server using a fake clock."""
IDLE_LIMIT = 900          # 15 minutes without activity
ABSOLUTE_LIMIT = 28800    # 8 hours since login


class Sessions:
    def __init__(self):
        self.store = {}

    def login(self, sid, now):
        self.store[sid] = {"created": now, "last_seen": now}

    def check(self, sid, now):
        s = self.store.get(sid)
        if s is None:
            return "rejected: unknown session"
        if now - s["created"] > ABSOLUTE_LIMIT:
            del self.store[sid]
            return "rejected: absolute timeout"
        if now - s["last_seen"] > IDLE_LIMIT:
            del self.store[sid]
            return "rejected: idle timeout"
        s["last_seen"] = now
        return "ok"


if __name__ == "__main__":
    s = Sessions()
    s.login("a", 0)
    r1 = s.check("a", 600)            # active within idle window
    r2 = s.check("a", 600 + 1000)     # idle for 1000 s
    s.login("b", 0)
    for t in range(600, ABSOLUTE_LIMIT, 600):
        assert s.check("b", t) == "ok"   # continuous activity keeps the session alive
    r3 = s.check("b", ABSOLUTE_LIMIT + 1)
    for name, r in (("active", r1), ("idle too long", r2), ("past absolute limit", r3)):
        print(f"{name:20} {r}")
    assert r1 == "ok"
    assert r2 == "rejected: idle timeout"
    assert r3 == "rejected: absolute timeout"
    print("PASS: both timeouts are enforced on the server for every request.")
    print("Review: cookie expiry alone is not enforcement; always check server-side state.")
