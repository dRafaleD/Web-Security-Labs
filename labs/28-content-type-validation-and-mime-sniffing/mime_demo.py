"""Validate declared content types against file signatures for synthetic uploads."""
SIGNATURES = {"image/png": b"\x89PNG", "image/jpeg": b"\xff\xd8\xff", "application/pdf": b"%PDF"}


def check(declared, filename, data):
    expected = SIGNATURES.get(declared)
    if expected is None:
        return "rejected: type not allowed"
    if not data.startswith(expected):
        return "rejected: content does not match declared type"
    ext = filename.rsplit(".", 1)[-1].lower()
    if declared.split("/")[1].replace("jpeg", "jpg") != ext:
        return "rejected: extension does not match declared type"
    return "accepted"


if __name__ == "__main__":
    cases = [
        ("image/png", "photo.png", b"\x89PNG....."),
        ("image/png", "photo.png", b"<html><script>"),
        ("image/png", "photo.php", b"\x89PNG....."),
        ("text/html", "page.html", b"<html>"),
        ("application/pdf", "doc.pdf", b"%PDF-1.7"),
    ]
    results = [check(*c) for c in cases]
    for c, r in zip(cases, results):
        print(f"{c[0]:16} {c[1]:10} {r}")
    assert results[0] == "accepted" and results[4] == "accepted"
    assert all(r.startswith("rejected") for r in results[1:4])
    print("PASS: declared type, extension and leading bytes must all agree.")
    print("Review: signatures are a quick check; serve uploads with nosniff and from a separate origin.")
