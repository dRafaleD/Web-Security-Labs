from pathlib import Path
ALLOWED={".txt", ".md"}
def validate(name,data):
    path=Path(name)
    if path.name!=name or name in {".",".."}:return False
    if path.suffix.lower() not in ALLOWED or not (0<len(data)<=1024):return False
    return b"\x00" not in data
if __name__=="__main__":
    for n,b in [("report.txt",b"training"),("../secret.txt",b"bad"),("run.exe",b"MZ"),("big.md",b"A"*1025)]:
        print(n,validate(n,b))
