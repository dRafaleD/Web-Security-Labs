seen={}
def create(request_id,owner,payload):
    key=(owner,request_id)
    if key in seen:
        if seen[key]["payload"] != payload: return "CONFLICT"
        return seen[key]["result"]
    result=f"created-{len(seen)+1}"
    seen[key]={"payload":payload,"result":result}
    return result
if __name__=="__main__":
    print(create("request-1","student","safe-note"))
    print(create("request-1","student","safe-note"))
    print(create("request-1","student","other-note"))
    assert len(seen)==1
