"""Offline receipt lookup. A receipt describes a prior action, not a new grant."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Receipt:
    actor: str
    resource: str
    operation: str
    version: int

RECEIPTS = {
    ("alice", "doc-a", "request-1"): Receipt("alice","doc-a","update-label",2)
}

def lookup(actor, resource, key, now_version, allowed):
    if not allowed or actor != "alice" or resource != "doc-a":
        return "DENY_SCOPE"
    item = RECEIPTS.get((actor,resource,key))
    if item is None:
        return "UNKNOWN_OPERATION"
    if now_version < item.version:
        return "STATE_REGRESSION_REVIEW"
    if now_version == item.version:
        return "COMMITTED_VERSION"
    return "COMMITTED_HISTORICAL_VERSION"

def main():
    cases = [
        ("alice","doc-a","request-1",2,True,"COMMITTED_VERSION"),
        ("alice","doc-a","request-1",3,True,"COMMITTED_HISTORICAL_VERSION"),
        ("alice","doc-a","request-1",1,True,"STATE_REGRESSION_REVIEW"),
        ("alice","doc-a","missing",2,True,"UNKNOWN_OPERATION"),
        ("alice","doc-a","request-1",2,False,"DENY_SCOPE"),
        ("bob","doc-a","request-1",2,True,"DENY_SCOPE"),
        ("alice","doc-b","request-1",2,True,"DENY_SCOPE"),
    ]
    for *args, expected in cases:
        actual = lookup(*args)
        assert actual == expected, (actual, expected)
        print(actual)
    print(f"{len(cases)}/{len(cases)} receipt checks passed")

if __name__ == "__main__":
    main()
