def audit(header):
    name_value, *attrs = [part.strip() for part in header.split(";")]
    flags = {a.split("=")[0].lower(): (a.split("=", 1)[1] if "=" in a else True) for a in attrs}
    problems = []
    if "secure" not in flags:
        problems.append("missing Secure")
    if "httponly" not in flags:
        problems.append("missing HttpOnly")
    if str(flags.get("samesite", "")).lower() not in {"lax", "strict"}:
        problems.append("SameSite not Lax/Strict")
    return name_value.split("=")[0], problems
if __name__ == "__main__":
    for h in ["sid=abc; Secure; HttpOnly; SameSite=Lax", "sid=abc; Path=/", "pref=dark; Secure; SameSite=None"]:
        print(audit(h))
