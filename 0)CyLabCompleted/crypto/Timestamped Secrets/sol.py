from hashlib import sha256
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def decrypt(ct: str) -> str:
    timestamp = int("1770242633")
    key = sha256(str(timestamp).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    # padded = pad(plaintext.encode(), AES.block_size)
    padded = cipher.decrypt(ct)
    pt = unpad(padded, AES.block_size).decode()
    return pt

ct = bytes.fromhex("6d8330b05a68848fdf4b7ab057cd6eb070810e3febd76872b4a5e7627221a396")

print(decrypt(ct))