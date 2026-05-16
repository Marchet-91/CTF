from pwn import *
from Crypto.Random.random import * 
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from math import gcd

HOST = "easyrsa.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)

io.recvline()
io.recvline()
io.recvline()
e = int(io.recvline().decode().strip().split(" ")[-1])
N = int(io.recvline().decode().strip().split(" ")[-1])


p, q = getPrime(512), getPrime(512)
while gcd((p-1)*(q-1), e) != 1:
    p, q = getrandbits(512), getrandbits(512)
io.sendlineafter(b":\n", str(p*q).encode())

io.recvline()
io.sendline(str(pow(bytes_to_long(b"Give me the flag"), e, N)).encode())

io.recvline()
io.recvline()
resp = io.recvline()
# print(resp)
ct = int(resp.decode().strip().split(" ")[-1])
print(ct)

d = pow(e, -1, (p-1)*(q-1))

print("pt: ", gcd((p-1)*(q-1), e))

pt = long_to_bytes(pow(ct, d, p*q))

print(pt.decode())

io.close()