"""Check pinned requirements against a synthetic advisory list and reject unpinned ones."""
ADVISORIES = {"examplelib": [("1.2.0", "1.2.9", "fixed in 1.3.0")], "otherlib": [("2.0.0", "2.0.3", "fixed in 2.0.4")]}
REQUIREMENTS = ["examplelib==1.2.5", "otherlib==2.0.4", "toolkit>=3.0", "helper==0.9.1"]


def parse_version(v):
    return tuple(int(x) for x in v.split("."))


def check(requirement):
    if "==" not in requirement:
        return "rejected: not pinned to an exact version"
    name, version = requirement.split("==")
    for low, high, note in ADVISORIES.get(name, []):
        if parse_version(low) <= parse_version(version) <= parse_version(high):
            return f"VULNERABLE: {note}"
    return "ok"


if __name__ == "__main__":
    for r in REQUIREMENTS:
        print(f"{r:20} {check(r)}")
    assert check(REQUIREMENTS[0]).startswith("VULNERABLE")
    assert check(REQUIREMENTS[1]) == "ok" and check(REQUIREMENTS[3]) == "ok"
    assert check(REQUIREMENTS[2]).startswith("rejected")
    print("PASS: pinned versions are compared with advisories and ranges are refused.")
    print("Review: an advisory match is a lead; reachability and transitive dependencies still need review.")
