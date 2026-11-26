"""Offline DTO projection for fictional records, not a web service."""
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    tenant: str
    role: str

USERS={"alice":User("a","member"),"bob":User("a","member"),
       "auditor":User("a","auditor"),"carol":User("b","member")}
RECORDS={"r1":{"tenant":"a","owner":"alice","title":"Training",
               "status":"open","internal_note":"fictional note"}}

def response(actor,record_id):
    user=USERS.get(actor)
    if user is None:
        return 401,{}
    record=RECORDS.get(record_id)
    if record is None or record["tenant"]!=user.tenant:
        return 404,{}
    if actor==record["owner"]:
        keys=("title","status")
    elif user.role=="auditor":
        keys=("title",)
    else:
        return 404,{}
    return 200,{key:record[key] for key in keys}

def main():
    cases=[
        ("alice","r1",200,{"title":"Training","status":"open"}),
        ("auditor","r1",200,{"title":"Training"}),
        ("bob","r1",404,{}),
        ("carol","r1",404,{}),
        ("alice","missing",404,{}),
        ("unknown","r1",401,{}),
    ]
    for actor,ident,status,body in cases:
        assert response(actor,ident)==(status,body)
        print(actor,ident,status,body)
    RECORDS["r1"]["new_private_field"]="synthetic extra field"
    assert response("alice","r1")== (200,{"title":"Training","status":"open"})
    assert response("auditor","r1")== (200,{"title":"Training"})
    assert response("bob","r1")==response("bob","missing")
    print("9 DTO and response checks passed")

if __name__=="__main__":
    main()
