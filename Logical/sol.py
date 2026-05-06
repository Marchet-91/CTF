from pwn import *
import random

HOST = "logical.challs.cyberchallenge.it"
PORT = 38207

io = remote(HOST, PORT)

io.sendlineafter(b"> ", b"2")


ct = int(io.recvline().decode().strip())
print(ct)

io.close()