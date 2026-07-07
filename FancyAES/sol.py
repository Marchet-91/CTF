from pwn import *

def split(txt):
    blocks = []
    for i in range(0, len(txt), 16):
        blocks.append(txt[i:i+16])
    return blocks

io = remote("fancyaes.chall.srdnlen.it", 443, ssl=True)

io.recvline()
ct = bytes.fromhex(io.recvline().decode().split(" ")[-1])

blocks = split(ct)

print(len(blocks))