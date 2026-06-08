from pwn import * 
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

HOST = "corrupted.challs.olicyber.it"
PORT = 10604

p = 3
q = 2

io = remote(HOST, PORT)

io.sendlineafter(b": ", str(q).encode() + b" " + str(p).encode())

A = int(io.recvline().strip().split(b": ")[-1].decode()[0])
B = int(io.recvline().strip().split(b": ")[-1].decode()[0])
ct = b64decode(io.recvline().strip().split(b" ")[-1])

io.close()

# print(ct)

for a in range(p):
    for b in range(p):
        # print(a, b)
        if pow(q, a, p) == A and pow(q, b, p) == B:
            # print(a, b)
            Alice_Shared_secret = pow(B, a, p)
            Bob_Shared_secret = pow(A, b, p)
            Shared_secret = pow(q, a * b, p)
            key = (Shared_secret % (2**(8*16) - 1)).to_bytes(16, 'big')
            cipher = AES.new(key, AES.MODE_ECB)
            pt = cipher.decrypt(ct)
            print(unpad(pt, 16).decode())
            exit()

# io.interactive()