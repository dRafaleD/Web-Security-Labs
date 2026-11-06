"""Check synthetic passwords for minimum length and presence in a tiny breached list."""
BREACHED = {"password123456", "letmeinletmein", "qwertyuiop12"}
MIN_LEN = 12


def check(password):
    normalized = password.strip().lower()
    if len(password) < MIN_LEN:
        return "rejected: shorter than 12 characters"
    if normalized in BREACHED or normalized.rstrip("!1") in BREACHED:
        return "rejected: appears in the breached-password list"
    return "accepted"


if __name__ == "__main__":
    tests = ["short1!", "Password123456", "letmeinletmein!", "correct horse battery staple", "tr0ub4dor&3xx"]
    results = [check(t) for t in tests]
    for t, r in zip(tests, results):
        print(f"{t:30} {r}")
    assert results[0].startswith("rejected: shorter")
    assert results[1].startswith("rejected: appears") and results[2].startswith("rejected: appears")
    assert results[3] == "accepted" and results[4] == "accepted"
    print("PASS: length and a normalized breached-list check are enforced.")
    print("Review: pair this with rate limiting and MFA, and never log the password.")
