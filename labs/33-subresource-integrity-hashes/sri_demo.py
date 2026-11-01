import base64, hashlib
def sri(data, algorithm="sha384"):
    digest = hashlib.new(algorithm, data).digest()
    return f"{algorithm}-{base64.b64encode(digest).decode()}"
def verify(data, expected):
    algorithm = expected.split("-", 1)[0]
    if algorithm not in {"sha256", "sha384", "sha512"}:
        return False
    return sri(data, algorithm) == expected
if __name__ == "__main__":
    script = b"console.log('training script');\n"
    tag = sri(script)
    print(tag)
    print("unchanged:", verify(script, tag))
    print("modified:", verify(script + b"//x", tag))
    assert verify(script, tag) and not verify(script + b"//x", tag)
