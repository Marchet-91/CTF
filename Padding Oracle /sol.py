from pwn import *

HOST = "padding-oracle.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)

io.recvline()
ct = io.recvline().decode().strip()

ct = bytes.fromhex(ct)
size = len(ct)
flag = ""

while len(flag) != size:
    
    for x in range(256):
        tmp = ct[:-16] + bytes([ct[-16] ^ x ^ 1]) + ct[-16:]
        io.sendlineafter(b"What do you want to decrypt (in hex)? ", tmp.hex().encode())
        
        if b"incorrect" not in io.recvline():
            print(x)

io.close()