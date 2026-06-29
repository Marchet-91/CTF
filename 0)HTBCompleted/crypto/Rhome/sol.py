from pwn import *
from factordb.factordb import FactorDB
from sympy.ntheory.factor_ import factorint
from sympy.ntheory import discrete_log
from hashlib import sha256
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt(ss, flag_part):
    key = sha256(long_to_bytes(ss)).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.decrypt(flag_part)
    return f"pt = {unpad(ct, 16)}"

HOST = "154.57.164.67"
PORT = 31647

io = remote(HOST, PORT)
# io.interactive()
io.recvline()
io.sendlineafter(b"> ", b"1")
# io.sendlineafter(b"> ", b"2")
# io.interactive(1)

p = int(io.recvline().decode().split("=")[-1].strip())
g = int(io.recvline().decode().split("=")[-1].strip())
A = int(io.recvline().decode().split("=")[-1].strip())
B = int(io.recvline().decode().split("=")[-1].strip())

io.sendlineafter(b"> ", b"3")
ct = bytes.fromhex(io.recvline().decode().split("=")[-1].strip())
io.close()

q = (p-1) // 2
f = factorint(q, limit=2**42)

q, r = sorted(f.keys())
dr = pow(r*2, -1, p)
h = pow(g, dr, p)
a, b = discrete_log(p, A, g), discrete_log(p, B, g)
ss = pow(A, b, p)

print(decrypt(ss, ct))