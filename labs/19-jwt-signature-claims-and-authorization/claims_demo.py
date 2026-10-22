from datetime import datetime,timezone
def authorize(verified, claims, tenant):
    if not verified or not isinstance(claims,dict): return False
    if claims.get("iss")!="training-issuer" or claims.get("aud")!="training-api": return False
    if claims.get("exp",0)<=datetime.now(timezone.utc).timestamp(): return False
    return claims.get("tenant")==tenant and claims.get("role")=="reader"
if __name__=="__main__":
    future=int(datetime.now(timezone.utc).timestamp())+60
    c={"iss":"training-issuer","aud":"training-api","exp":future,"tenant":"a","role":"reader"}
    assert authorize(True,c,"a")
    assert not authorize(False,c,"a")
    assert not authorize(True,c,"b")
    print("Claim validation simulation passed; this is NOT a JWT signature verifier.")
