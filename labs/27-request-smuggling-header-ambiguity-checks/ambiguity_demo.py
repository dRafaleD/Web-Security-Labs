"""Reject HTTP requests whose framing headers are ambiguous (defensive validator)."""


def validate(headers):
    names = [k.lower() for k, _ in headers]
    cl = [v for k, v in headers if k.lower() == "content-length"]
    if "transfer-encoding" in names and cl:
        return "rejected: both Content-Length and Transfer-Encoding"
    if len(cl) > 1 and len(set(cl)) > 1:
        return "rejected: conflicting Content-Length values"
    if cl and not cl[0].isdigit():
        return "rejected: malformed Content-Length"
    if names.count("transfer-encoding") > 1:
        return "rejected: duplicate Transfer-Encoding"
    return "accepted"


if __name__ == "__main__":
    cases = {
        "plain": [("Host", "a.test"), ("Content-Length", "10")],
        "both": [("Content-Length", "10"), ("Transfer-Encoding", "chunked")],
        "conflict": [("Content-Length", "10"), ("Content-Length", "11")],
        "malformed": [("Content-Length", "+10")],
        "chunked": [("Transfer-Encoding", "chunked")],
    }
    for name, headers in cases.items():
        print(f"{name:10} {validate(headers)}")
    assert validate(cases["plain"]) == "accepted" and validate(cases["chunked"]) == "accepted"
    assert all(validate(cases[k]).startswith("rejected") for k in ("both", "conflict", "malformed"))
    print("PASS: ambiguous framing is rejected instead of guessed.")
    print("Review: all servers on the path must parse consistently; HTTP/2 end to end helps.")
