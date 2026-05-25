#!/usr/bin/env python3

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

FLAG = os.environ['FLAG'].encode()

KEY = os.urandom(32)
MENU = """
What do you want to do?
1) Encrypt your message
2) Decrypt your message
3) Exit
"""
# A - B - C - D
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
    # 4) d(I) ^ e(A) ^ I

    # 0) I
    # 1) d(e(D) ^ C) ^ I
    # 2) d(e(C) ^ B) ^ e(D) ^ C
    # 3) d(e(B) ^ A) ^ e(C) ^ B
    # 4) d(e(A) ^ I) ^ e(B) ^ A
    # 5) d(I) ^ e(A) ^ I
    ct = blocks2[::-1]
    return b"".join(ct)


# I B C D E F G
def decrypt(ct):
    global KEY
    cipher = AES.new(KEY, AES.MODE_ECB)

    blocks2 = [ct[i:i + 16] for i in range(0, len(ct), 16)][::-1]
    nonce = blocks2[0]

    blocks1 = [nonce]
    for i in range(len(blocks2) - 1): 
        tmp = bytes(x ^ y for x, y in zip(blocks1[i], blocks2[i + 1]))
        blocks1 += [cipher.encrypt(tmp)]

    blocks0 = [nonce]
    for i in range(len(blocks1) - 1):
        tmp = bytes(x ^ y for x, y in zip(blocks0[i], blocks1[-(i + 1)]))
        blocks0 += [cipher.decrypt(tmp)]
    msg = blocks0[1:]
    return b"".join(msg)


print(f"I have developed a new AES shema that will become the new standard!")
print(f"You have early access ^w^ and you will never decrypt my flag: {encrypt(FLAG).hex()}")

while True:
    try:
        print(MENU)
        choice = int(input("> "))

        if choice == 1:
            msg = bytes.fromhex(input("> (hex) "))
            ct = encrypt(msg)
            print(f"Here's your message securely encrypted ^w^: {ct.hex()}")
        elif choice == 2:
            ct = bytes.fromhex(input("> (hex) "))
            msg = decrypt(ct)
            print(f"Here's your decrypted message... Oh no, I'm sorry, you can't have it :P")  
        elif choice == 3:
            print("See you later.... Byeee!")
            break
        else:
            print(f"I see... The {choice} choice, you're clever ^w^")
    except:
        print("Erhm... Are you okay?")
