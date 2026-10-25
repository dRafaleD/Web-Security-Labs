import unicodedata
def normalize(name):
    return unicodedata.normalize("NFKC", name).strip().casefold()
def is_valid(name):
    return name.isascii() and name.isalnum() and 3 <= len(name) <= 16
def register(name, taken):
    canonical = normalize(name)
    if not is_valid(canonical):
        return "rejected"
    if canonical in taken:
        return "duplicate"
    taken.add(canonical)
    return "ok:" + canonical
if __name__ == "__main__":
    taken = set()
    for n in ["Alice", "ALICE", "Ａlice", " alice ", "a/b", "al"]:
        print(repr(n), "->", register(n, taken))
