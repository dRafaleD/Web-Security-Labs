"""Offline access-policy matrix, not a running HTTP server."""
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    tenant: str
    role: str

@dataclass(frozen=True)
class Record:
    tenant: str
    owner: str

USERS={"alice":User("a","member"),"bob":User("a","member"),
       "admin":User("a","admin"),"carol":User("b","member")}
RECORDS={"doc-a":Record("a","alice"),"doc-b":Record("b","carol")}

def respond(actor, record_id, method):
    if actor not in USERS:
        return 401
    if method not in {"GET","PATCH"}:
        return 405
    user=USERS[actor]
    record=RECORDS.get(record_id)
    if record is None or record.tenant!=user.tenant:
        return 404
    if actor!=record.owner and user.role!="admin":
        return 404
    if method=="PATCH" and actor!=record.owner:
        return 403
    return 200

def main():
    cases=[
        ("alice","doc-a","GET",200),
        ("alice","doc-a","PATCH",200),
        ("bob","doc-a","GET",404),
        ("bob","doc-a","PATCH",404),
        ("admin","doc-a","GET",200),
        ("admin","doc-a","PATCH",403),
        ("admin","doc-b","GET",404),
        ("alice","doc-b","GET",404),
        ("alice","missing","GET",404),
        ("carol","doc-b","GET",200),
        ("carol","doc-b","PATCH",200),
        ("carol","doc-a","GET",404),
        ("unknown","doc-a","GET",401),
        ("alice","doc-a","DELETE",405),
        ("alice","doc-a","POST",405),
    ]
    for actor,record,method,expected in cases:
        actual=respond(actor,record,method)
        assert actual==expected,(actor,record,method,actual)
        print(f"{actor:8} {record:8} {method:7} {actual}")
    assert respond("bob","doc-a","GET")==respond("bob","missing","GET")
    print("15 cases + 1 response-consistency check passed")

if __name__=="__main__":
    main()
