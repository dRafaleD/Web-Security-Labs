from urllib.parse import urlparse
ALLOWED_HOSTS = {"app.example.test"}
def safe_redirect(target, default="/home"):
    if target.startswith("/") and not target.startswith("//") and "\\" not in target:
        return target
    parsed = urlparse(target)
    if parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS:
        return target
    return default
if __name__ == "__main__":
    for t in ["/account", "//evil.test/x", "https://app.example.test/a", "https://app.example.test.evil.test/a", "javascript:alert(1)"]:
        print(t, "->", safe_redirect(t))
