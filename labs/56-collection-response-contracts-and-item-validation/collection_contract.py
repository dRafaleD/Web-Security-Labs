"""Offline validation of a fictional paginated response."""
def check(payload):
    if not isinstance(payload,dict) or set(payload)!={"items","count"}:
        return "INVALID_ENVELOPE"
    items,count=payload["items"],payload["count"]
    if not isinstance(items,list) or len(items)>3:
        return "INVALID_COLLECTION"
    if type(count) is not int or count!=len(items):
        return "INVALID_COUNT"
    seen=set()
    for item in items:
        if not isinstance(item,dict) or set(item)!={"id","title"}:
            return "INVALID_ITEM_FIELDS"
        if not all(isinstance(v,str) and v for v in item.values()):
            return "INVALID_ITEM_TYPE"
        if item["id"] in seen:
            return "DUPLICATE_ID"
        seen.add(item["id"])
    return "CONTRACT_OK"

def main():
    a={"id":"a","title":"Sample"}
    b={"id":"b","title":"Other"}
    cases=[
        ({"items":[],"count":0},"CONTRACT_OK"),
        ({"items":[a,b],"count":2},"CONTRACT_OK"),
        ({"items":[a],"count":2},"INVALID_COUNT"),
        ({"items":[a],"count":True},"INVALID_COUNT"),
        ({"items":[a,a],"count":2},"DUPLICATE_ID"),
        ({"items":[a,{**b,"private_note":"toy"}],"count":2},"INVALID_ITEM_FIELDS"),
        ({"items":[{"id":"a"}],"count":1},"INVALID_ITEM_FIELDS"),
        ({"items":[{"id":3,"title":"x"}],"count":1},"INVALID_ITEM_TYPE"),
        ({"items":[a]*4,"count":4},"INVALID_COLLECTION"),
        ({"items":{},"count":0},"INVALID_COLLECTION"),
        ({"items":[],"count":0,"extra":1},"INVALID_ENVELOPE"),
    ]
    for payload,expected in cases:
        result=check(payload)
        assert result==expected,(payload,result)
        print(result)
    print("11/11 collection checks passed")

if __name__ == "__main__":
    main()
