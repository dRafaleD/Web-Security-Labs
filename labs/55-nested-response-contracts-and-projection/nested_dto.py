"""Offline projection of fictional nested records; no server or real data."""
def project(record):
    if not isinstance(record,dict) or not isinstance(record.get("profile"),dict):
        return None
    profile=record["profile"]
    if not isinstance(record.get("id"),str) or not isinstance(profile.get("name"),str):
        return None
    return {"id":record["id"],"profile":{"name":profile["name"]}}

def verify(value):
    if not isinstance(value,dict) or set(value)!={"id","profile"}:
        return False
    profile=value["profile"]
    return (isinstance(value["id"],str) and isinstance(profile,dict)
            and set(profile)=={"name"} and isinstance(profile["name"],str))

def main():
    raw={"id":"demo","profile":{"name":"Ada","private_note":"fictional"},
         "internal_status":"draft"}
    good={"id":"demo","profile":{"name":"Ada"}}
    assert project(raw)==good
    assert project({"id":4,"profile":{"name":"Ada"}}) is None
    assert project({"id":"demo","profile":None}) is None
    cases=[
        (good,True),
        (raw,False),
        ({"id":"demo","profile":raw["profile"]},False),
        ({"id":"demo","profile":{}},False),
        ({"id":"demo","profile":{"name":4}},False),
        ({"id":"demo","profile":"Ada"},False),
        ({"id":False,"profile":{"name":"Ada"}},False),
        (None,False),
    ]
    for value,want in cases:
        got=verify(value)
        assert got==want,(got,want)
        print("CONTRACT_OK" if got else "REJECT")
    print("8 contract cases + 3 projection checks passed")

if __name__=="__main__":
    main()
