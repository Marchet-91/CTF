from pwn import *
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(msg):
    global KEY
    cipher = AES.new(KEY, AES.MODE_ECB)

    pad_msg = pad(msg, 16)
    nonce = os.urandom(16)
    # I A B C D 
    blocks0 = [nonce] + [pad_msg[i:i + 16] for i in range(0, len(pad_msg), 16)]

    # I A B C D             0
    blocks1 = [nonce]
    for i in range(len(blocks0) - 1):
        tmp = cipher.encrypt(blocks0[i + 1])
        blocks1 += [bytes(x ^ y for x, y in zip(tmp, blocks0[i]))]
    # 0) e(A) ^ I 
    # 1) e(B) ^ A
    # 2) e(C) ^ B
    # 3) e(D) ^ C

    # I - e(A) ^ I - e(B) ^ A - e(C) ^ B - e(D) ^ C
    blocks2 = [nonce]
    for i in range(len(blocks1) - 1):
        tmp = cipher.decrypt(blocks1[-(i + 1)])
        blocks2 += [bytes(x ^ y for x, y in zip(tmp, blocks1[-i]))]
    # 0) d(e(D) ^ C) ^ I
    # 1) d(e(C) ^ B) ^ e(D) ^ C
    # 2) d(e(B) ^ A) ^ e(C) ^ B
    # 3) d(e(A) ^ I) ^ e(B) ^ A

    # 0) I
    # 1) d(e(D) ^ C) ^ I
    # 2) d(e(C) ^ B) ^ e(D) ^ C
    # 3) d(e(B) ^ A) ^ e(C) ^ B
    # 4) d(e(A) ^ I) ^ e(B) ^ A
    ct = blocks2[::-1]
    return b"".join(ct)

HOST = "fancyaes.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)

io.recvline()
ct = io.recvline().split(b" ")[-1].decode()
ct = ct[::-1]
ct = bytes.fromhex(ct)
print(len(ct) / 16)

io.close()


