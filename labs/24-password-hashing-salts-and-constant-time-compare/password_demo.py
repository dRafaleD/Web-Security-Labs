import hashlib, hmac, os
N, R, P = 2**14, 8, 1
def hash_password(password, salt=None):
    salt = salt or os.urandom(16)
    return salt, hashlib.scrypt(password.encode(), salt=salt, n=N, r=R, p=P)
def verify(password, salt, expected):
    _, candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, expected)
if __name__ == "__main__":
    s1, h1 = hash_password("correct horse")
    s2, h2 = hash_password("correct horse")
    print("same password, different salt -> different hash:", h1 != h2)
    print("right password:", verify("correct horse", s1, h1))
    print("wrong password:", verify("wrong", s1, h1))
    assert verify("correct horse", s1, h1) and not verify("wrong", s1, h1)
