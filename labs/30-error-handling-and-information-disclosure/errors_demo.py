"""Return generic errors with a correlation ID while keeping details in the server log."""
import uuid

SERVER_LOG = []


def handle(request):
    try:
        if request == "missing-user":
            raise KeyError("user 'alice' not found in table accounts")
        if request == "db-error":
            raise RuntimeError("SELECT * FROM accounts WHERE id=7 failed at /srv/app/db.py:88")
        return {"status": 200, "body": "ok"}
    except Exception as exc:                      # noqa: BLE001 (demo)
        cid = uuid.uuid4().hex[:8]
        SERVER_LOG.append((cid, repr(exc)))
        return {"status": 500, "body": f"Something went wrong. Reference: {cid}"}


if __name__ == "__main__":
    responses = [handle(r) for r in ("ok", "missing-user", "db-error")]
    for r in responses:
        print(r)
    print("server log entries:", len(SERVER_LOG))
    assert responses[0]["status"] == 200
    assert responses[1]["body"].split(": ")[0] == responses[2]["body"].split(": ")[0], "same generic text"
    assert all(s not in r["body"] for r in responses for s in ("alice", "SELECT", "/srv"))
    assert len(SERVER_LOG) == 2
    print("PASS: users get a generic message and a reference; details stay in the log.")
    print("Review: also keep timing and status codes consistent to avoid enumeration.")
