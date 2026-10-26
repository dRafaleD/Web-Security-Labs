"""Login throttling: per-account and per-IP counters with a uniform error message."""
import time


class Throttle:
    def __init__(self, max_fail=5, window=300):
        self.max_fail, self.window, self.fails = max_fail, window, {}

    def _count(self, key, now):
        self.fails[key] = [t for t in self.fails.get(key, []) if now - t < self.window]
        return len(self.fails[key])

    def blocked(self, user, ip, now):
        return self._count(("u", user), now) >= self.max_fail or self._count(("ip", ip), now) >= self.max_fail * 4

    def record_failure(self, user, ip, now):
        for key in (("u", user), ("ip", ip)):
            self.fails.setdefault(key, []).append(now)


USERS = {"alice": "correct horse"}
MESSAGE = "Invalid credentials or too many attempts"   # uniform: no username enumeration


def login(throttle, user, password, ip, now):
    if throttle.blocked(user, ip, now):
        return MESSAGE
    if USERS.get(user) == password:
        return "ok"
    throttle.record_failure(user, ip, now)
    return MESSAGE


if __name__ == "__main__":
    t, now = Throttle(), time.time()
    for i in range(5):
        login(t, "alice", f"guess{i}", "198.51.100.1", now + i)
    locked = login(t, "alice", "correct horse", "198.51.100.1", now + 6)
    later = login(t, "alice", "correct horse", "198.51.100.1", now + 400)
    unknown = login(t, "nobody", "x", "198.51.100.2", now + 401)
    print("right password while locked :", locked)
    print("after the window expires    :", later)
    print("unknown user message        :", unknown)
    assert locked != "ok" and later == "ok"
    assert unknown == locked
    print("PASS: repeated failures lock the account temporarily, with one uniform message.")
    print("Review: per-account lockout lets an attacker lock out victims; combine with IP limits and MFA.")
