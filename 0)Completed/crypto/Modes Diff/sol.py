from pwn import * 

def split(txt):
    blocks = []
    for i in range(0, len(txt), 16):
        blocks.append(txt[i:i+16])

    return blocks

ct = bytes.fromhex("866bb5802051d56f37b1073a501b4afe4324424336ba60d4efe9af817b27a95a0f3adec8b809088bbaaebbfa0629c079")
iv = ct[:16]
ct = ct[16:]
io = remote("modes.challs.olicyber.it", 10802)

io.sendlineafter(b": ", ct.hex().encode())

ks = bytes.fromhex(io.recvline().decode())
ks = split(ks)
ct = split(ct)

pt = bytes(xor(iv, ks[0]) + xor(ks[1], ct[0])).decode()

print(pt)
