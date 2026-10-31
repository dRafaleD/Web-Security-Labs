"""Compare a seeded general-purpose generator with the secrets module for tokens."""
import random
import secrets


def weak_token(seed):
    rng = random.Random(seed)
    return "%032x" % rng.getrandbits(128)


def strong_token():
    return secrets.token_hex(16)   # 128 bits from the OS CSPRNG


if __name__ == "__main__":
    a, b = weak_token(1234), weak_token(1234)
    s1, s2 = strong_token(), strong_token()
    print("weak  :", a, b, "same =", a == b)
    print("strong:", s1, s2, "same =", s1 == s2)
    bits = len(s1) * 4
    print("strong token bits:", bits)
    assert a == b, "a known seed reproduces the token"
    assert s1 != s2 and bits == 128
    print("PASS: seeded generators are reproducible; the secrets module is not.")
    print("Review: 32 hex characters of a predictable source are still predictable.")
