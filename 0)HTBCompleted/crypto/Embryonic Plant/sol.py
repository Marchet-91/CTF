from pwn import *
import math
from factordb.factordb import FactorDB
import ast
from hashlib import sha256
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST = "154.57.164.76"
PORT = 30600

# io = process(["python3", "server.py"])
io = remote(HOST, PORT)

n = int(io.recvline().decode().split("=")[-1].strip())
s = ast.literal_eval(io.recvline().decode().split("=")[-1])
ct = bytes.fromhex(io.recvline().decode().split("=")[-1].strip())
e = 0x10001
io.close()

a = (s[2]-s[1])*(s[3]-s[2])
b = (s[1]-s[0])*(s[4]-s[3])


r = math.gcd(a-b, n)
p = ((s[2]-s[1])*pow(s[1]-s[0], -1,r)) % r
q = (n // r) // p
fi = (p-1)*(q-1)*(r-1)
d = pow(e, -1, fi)
key = sha256(long_to_bytes(d)).digest()
cipher = AES.new(key, AES.MODE_ECB)
pt = unpad(cipher.decrypt(ct), 16)
print(pt.decode())

# io.interactive()