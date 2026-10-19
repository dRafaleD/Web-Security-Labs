import secrets,hashlib
from datetime import datetime,timedelta,timezone
records={}
def issue(user):
    token=secrets.token_urlsafe(32)
    records[hashlib.sha256(token.encode()).hexdigest()]=(user,datetime.now(timezone.utc)+timedelta(minutes=10))
    return token
def consume(token):
    key=hashlib.sha256(token.encode()).hexdigest()
    row=records.pop(key,None)
    return row[0] if row and datetime.now(timezone.utc)<row[1] else None
if __name__=="__main__":
    token=issue("student")
    print("first",consume(token))
    print("replay",consume(token))
