from hashlib import sha256
from datetime import datetime
import random
from pwn import xor

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

dt = datetime.strptime("2021-03-21 17:37:40", "%Y-%m-%d %H:%M:%S")

ts = int(datetime.timestamp(dt))
h = sha256(int_to_bytes(ts)).digest()
seed = int_from_bytes(h[32:])
key = h[:32]

random.seed(seed)
for _ in range(32):
    key += bytes([random.randint(0, 255)])

print(open("bho", "wb").write(xor(open("flag.enc", "rb").read())))