from pwn import * 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def split(txt):
    blocks = []
    for i in range(0, len(txt), 16):
        blocks.append(txt[i:i+16])
    return blocks

def encrypt(msg, n):
    # global KEY
    # cipher = AES.new(KEY, AES.MODE_ECB)

    pos = 0
    par = ["()"]

    # pad_msg = pad(msg, 16)
    nonce = "I" + str(n)
    blocks0 = [nonce] + msg
    # I
    # d(e(6) ^ 5) = 1
    # d(e(1) ^ I) ^ (e(2) ^ 1) = 6

    blocks1 = [nonce]
    for i in range(len(blocks0) - 1): # 0 - 7-1
        tmp = f"e{par[pos][0]}{blocks0[i + 1]}{par[pos][1]}"
        pos = (pos + 1) % 1
        blocks1 += [f"{tmp} ^ {blocks0[i]}"]
    # I
    # e(6) ^ 5 ^ I
    # e(d(e(1) ^ I) ^ (e(2) ^ 1)) ^ d(e(6) ^ 5)

    blocks2 = [nonce]
    for i in range(len(blocks1) - 1): # 0 - 7-1
        tmp = f"d{par[pos][0]}{blocks1[-(i + 1)]}{par[pos][1]}"
        pos = (pos + 1) % 1
        blocks2 += [f"{tmp} ^ {blocks1[-i]}"]
    return blocks2

io = remote("fancyaes.chall.srdnlen.it", 443, ssl=True)
io.recvline()
ct = split(bytes.fromhex(io.recvline().decode().split(" ")[-1]))[::-1]

pt = ["d(e(6) ^ 5)", "d(e(6) ^ 5)","d(e(6) ^ 5)","PAD"]

def calcolo(blocks, ct, pad):
    a = blocks[3] # d(e(d(e(6) ^ 5)) ^ d(e(6) ^ 5)) ^ e(d(e(6) ^ 5)) ^ d(e(6) ^ 5)
    b = ct # d(e(6) ^ 5)
    c = xor(xor(blocks[2], pad),ct) # d(e(PAD) ^ d(e(6) ^ 5))
    enc = xor(xor(a, b),c) # e(6) ^ 5
    return enc

def send(txt, cond=True):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"> (hex) ",txt.encode())
    resp = io.recvline().decode().split(" ")[-1].strip()
    enc = split(bytes.fromhex(resp))[::-1]

    # print(("\x00"*32).hex())
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"> (hex) ",(b"\x00"*32).hex().encode())
    resp = io.recvline().decode().split(" ")[-1].strip()
    pad = split(bytes.fromhex(resp))[::-1][2]
    if cond: 
        # print(enc)
        enc = calcolo(enc, bytes.fromhex(txt)[:16], pad)
    return enc, pad

iv = ct[0]
enc = []

pt = ["1", "2", "3", "4", "5", "6"]
# 0 I0
# 1 d(e(6) ^ 5) ^ I0
# 2 d(e(5) ^ 4) ^ e(6) ^ 5
# 3 d(e(4) ^ 3) ^ e(5) ^ 4
# 4 d(e(3) ^ 2) ^ e(4) ^ 3
# 5 d(e(2) ^ 1) ^ e(3) ^ 2
# 6 d(e(1) ^ I0) ^ e(2) ^ 1


tmp = xor(iv, ct[1])
tmp = (tmp * 3).hex()
enc.append(send(tmp)[0]) # e(6) ^ 5

tmp = xor(enc[0], ct[2])
tmp = (tmp * 3).hex()
enc.append(send(tmp)[0]) # e(5) ^ 4

tmp = xor(enc[1], ct[3])
tmp = (tmp * 3).hex()
enc.append(send(tmp)[0]) # e(4) ^ 3

tmp = xor(enc[2], ct[4])
tmp = (tmp * 3).hex()
enc.append(send(tmp)[0]) # e(3) ^ 2

tmp = xor(enc[3], ct[5])
tmp = (tmp * 3).hex()
enc.append(send(tmp)[0]) # e(2) ^ 1

tmp = xor(enc[4], ct[6])
tmp = (tmp * 3).hex()
enc.append(send(tmp)[0]) # e(1) ^ I0

pt = ["1", "2", "3", "4", "5", "6"]
# 0 I0
# 1 d(e(6) ^ 5) ^ I0
# 2 d(e(5) ^ 4) ^ e(6) ^ 5
# 3 d(e(4) ^ 3) ^ e(5) ^ 4
# 4 d(e(3) ^ 2) ^ e(4) ^ 3
# 5 d(e(2) ^ 1) ^ e(3) ^ 2
# 6 d(e(1) ^ I0) ^ e(2) ^ 1

dec = []
dec.append(xor(ct[1], iv)) # d(e(6) ^ 5)
dec.append(xor(ct[2], enc[0])) # d(e(5) ^ 4)
dec.append(xor(ct[3], enc[1])) # d(e(4) ^ 3)
dec.append(xor(ct[4], enc[2])) # d(e(3) ^ 2)
dec.append(xor(ct[5], enc[3])) # d(e(2) ^ 1)
dec.append(xor(ct[6], enc[4])) # d(e(1) ^ I0)

tmp = (dec[-1] * 3).hex()
resp, pad = send(tmp, False)
b = xor(xor(resp[4], dec[-1]), enc[-1])
a = xor(resp[0],iv).hex() + b.hex()
resp1, pad = send(a, False)
tmp = xor(resp1[2], b)
pt = [xor(tmp, pad)]

tmp = (dec[-2] * 3).hex()
resp, pad = send(tmp, False)
b = xor(xor(resp[4], dec[-2]), enc[-2])
a = xor(resp[0], pt[0]).hex() + b.hex()
resp1, pad = send(a, False)
tmp = xor(resp1[2], b)
pt += [xor(tmp, pad)]

tmp = (dec[-3] * 3).hex()
resp, pad = send(tmp, False)
b = xor(xor(resp[4], dec[-3]), enc[-3])
a = xor(resp[0], pt[1]).hex() + b.hex()
resp1, pad = send(a, False)
tmp = xor(resp1[2], b)
pt += [xor(tmp, pad)]

tmp = (dec[-4] * 3).hex()
resp, pad = send(tmp, False)
b = xor(xor(resp[4], dec[-4]), enc[-4])
a = xor(resp[0], pt[2]).hex() + b.hex()
resp1, pad = send(a, False)
tmp = xor(resp1[2], b)
pt += [xor(tmp, pad)]

tmp = (dec[-5] * 3).hex()
resp, pad = send(tmp, False)
b = xor(xor(resp[4], dec[-5]), enc[-5])
a = xor(resp[0], pt[3]).hex() + b.hex()
resp1, pad = send(a, False)
tmp = xor(resp1[2], b)
pt += [xor(tmp, pad)]

tmp = (dec[-6] * 3).hex()
resp, pad = send(tmp, False)
b = xor(xor(resp[4], dec[-6]), enc[-6])
a = xor(resp[0], pt[4]).hex() + b.hex()
resp1, pad = send(a, False)
tmp = xor(resp1[2], b)
pt += [xor(tmp, pad)[:-8]]

print(b"".join(pt).decode())

io.close()

# srdnlen{cr3dits_t0_idek-ctf-2022*:_wh0_3v3n_c0m3s_up_w1th_r1d1cul0us_sch3m3s_l1k3_th3s3}