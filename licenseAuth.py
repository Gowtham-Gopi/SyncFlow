import hashlib
import os
import base64

SECRET_KEY = "PAPERPLANE"

def hashify(data: str) -> str:
    salted = data + SECRET_KEY
    sha256_hash = hashlib.sha256(salted.encode('utf-8')).digest()

    base32_string = base64.b32encode(sha256_hash).decode('utf-8').replace("=", "")
    short_hash = base32_string[:12]

    return short_hash

def getPrimary():
    computer_name = os.environ.get("COMPUTERNAME","DEFAULT_WIN_USER").lower()
    user_name = os.environ.get("USERNAME", "USER").lower()
    data = computer_name+user_name
    return hashify(data)

def verifyHash(inputHash: str):
    inputHash = inputHash.replace("-","").strip()
    secondary = hashify(getPrimary())
    if inputHash == secondary:
        return True
    else:
        return False


# License Key Generation:
# License Key is the base32 encoding of the sha256 digest of the primary key clipped to length 12