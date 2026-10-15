from hmac import compare_digest
ORIGIN="https://app.example.test"
TOKEN="synthetic-training-only"
def allowed(method,origin,session,token):
 if method in ("GET","HEAD"): return True
 if method not in ("POST","PUT","PATCH","DELETE"):return False
 return bool(session) and origin==ORIGIN and compare_digest(token or "",TOKEN)
tests=[("POST",ORIGIN,True,TOKEN,True),("POST","https://evil.example.test",True,TOKEN,False),("POST",ORIGIN,True,None,False),("POST",ORIGIN,False,TOKEN,False)]
for method,origin,session,token,want in tests:assert allowed(method,origin,session,token)==want
print("PASS four offline CSRF policy cases")