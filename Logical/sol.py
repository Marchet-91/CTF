from pwn import *
import random

def verifica(ct, n):
    ct = ct[n:]
    blocks = [ct[i: i + (2*n - 2)] for i in range(0,len(ct),2*n-2)]
    for i in blocks:
        if len(i) != 2*n - 2:
            return False, None
    return True, len(blocks)
    

def search_N(ct):
    for i in range(3, len(ct)):
        condition, size =  verifica(ct,i)
        if condition:
            print(i, size)

HOST = "logical.challs.cyberchallenge.it"
PORT = 38207

io = remote(HOST, PORT)

io.sendlineafter(b"> ", b"2")


ct = int(io.recvline().decode().strip())
# print(ct)
ct = bin(ct)[2:]
# print(len(ct))
search_N(ct)

io.close()