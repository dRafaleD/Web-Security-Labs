"""Offline DTO regression checks on invented records."""
CONTRACTS={"member":{"id","title"},"auditor":{"id","title","state"}}
RECORD={"id":"sample-1","title":"Practice","state":"ready",
        "internal_note":"fictional private field"}

def project(role,record):
    fields=CONTRACTS.get(role)
    if fields is None:
        return None
    return {key:record[key] for key in sorted(fields) if key in record}

def verify(role,response):
    fields=CONTRACTS.get(role)
    if fields is None:
        return "DENY_ROLE"
    if not isinstance(response,dict):
        return "INVALID_RESPONSE"
    if set(response)-fields:
        return "EXTRA_FIELDS"
    if fields-set(response):
        return "MISSING_FIELDS"
    if any(not isinstance(v,str) for v in response.values()):
        return "INVALID_TYPE"
    return "CONTRACT_OK"

def main():
    member=project("member",RECORD)
    auditor=project("auditor",RECORD)
    cases=[
        ("member",member,"CONTRACT_OK"),
        ("auditor",auditor,"CONTRACT_OK"),
        ("member",auditor,"EXTRA_FIELDS"),
        ("member",{**member,"internal_note":"note"},"EXTRA_FIELDS"),
        ("auditor",member,"MISSING_FIELDS"),
        ("member",{"id":"sample-1"},"MISSING_FIELDS"),
        ("member",{**member,"id":7},"INVALID_TYPE"),
        ("member",None,"INVALID_RESPONSE"),
        ("unknown",member,"DENY_ROLE"),
        ("member",project("member",{**RECORD,"extra":"new"}),"CONTRACT_OK"),
    ]
    for role,value,want in cases:
        got=verify(role,value)
        assert got==want,(role,got,want)
        print(role,got)
    assert project("unknown",RECORD) is None
    print("11/11 response-contract cases passed")

if __name__=="__main__":
    main()
