"""Local API authorization simulation; no server/network."""
ROWS={"1":{"owner":"alice","title":"A"},"2":{"owner":"bob","title":"B"}}
def read(actor,key):
 row=ROWS.get(key)
 return (200,{"title":row["title"]}) if row and row["owner"]==actor else (404,{"error":"not found"})
def update(actor,key,payload):
 row=ROWS.get(key)
 if not row or row["owner"]!=actor:return 404
 if not isinstance(payload,dict) or set(payload)!={"title"} or not isinstance(payload["title"],str):return 400
 row["title"]=payload["title"]
 return 200
if __name__=="__main__":
 assert read("alice","1")[0]==200
 assert read("alice","2")[0]==404
 assert update("alice","1",{"owner":"alice","title":"X"})==400
 assert update("alice","1",{"title":"Updated"})==200
 print("PASS BOLA and mass assignment negative tests")
