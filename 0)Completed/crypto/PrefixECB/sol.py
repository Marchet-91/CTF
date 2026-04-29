from pwn_template import *
from string import printable

HOST = "prefixecb.chall.srdnlen.it"
PORT = 443
SIZE = 16 

def encrypt(v):
    io.sendlineafter(b": ", v)
    io.recvline()
    risp = io.recvline().decode()
    return bytes.fromhex(risp)

io = remote(HOST, PORT, ssl=True)
flag = "srdnlen{0n3_byt3_4t_4_t1m3}"
plain = "A" * (SIZE + SIZE - (len(flag) + 1))

# print(plain)
ct = encrypt(plain.encode())
for i in printable:
    # print(i)
    guess = encrypt((plain + flag + i).encode())
    # print(ct, guess)
    if ct [16:32] == guess[16:32]:
        print(f"TROVATO: {i}")
        break

io.close()

# CCIT{