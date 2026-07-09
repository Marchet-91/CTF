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

def encrypt(msg):
    global KEY
    cipher = AES.new(KEY, AES.MODE_ECB)

    # A B C D E F
    pad_msg = pad(msg, 16)
    nonce = os.urandom(16)
    blocks0 = [nonce] + [pad_msg[i:i + 16] for i in range(0, len(pad_msg), 16)]
    # I 1 2 3 4 5 6

    blocks1 = [nonce]
    for i in range(len(blocks0) - 1):
        tmp = cipher.encrypt(blocks0[i + 1])
        blocks1 += [bytes(x ^ y for x, y in zip(tmp, blocks0[i]))]
    # I
    # e(1) ^ I
    # e(2) ^ A
    # e(3) ^ B
    # e(4) ^ C
    # e(5) ^ D
    # e(6) ^ E

    blocks2 = [nonce]
    for i in range(len(blocks1) - 1): # 5 - 7-1
        tmp = cipher.decrypt(blocks1[-(i + 1)])
        blocks2 += [bytes(x ^ y for x, y in zip(tmp, blocks1[-i]))]
    # d(e(F) ^ E) ^ I
    # d(e(E) ^ D) ^ (e(F) ^ E)
    # d(e(D) ^ C) ^ (e(E) ^ D)
    # d(e(C) ^ B) ^ (e(D) ^ C)
    # d(e(B) ^ A) ^ (e(C) ^ B)
    # d(e(A) ^ I) ^ (e(B) ^ A)

    # I
    ct = blocks2[::-1]
    return b"".join(ct)


def decrypt(ct):
    global KEY
    cipher = AES.new(KEY, AES.MODE_ECB)

    # A B C D E F G
    blocks2 = [ct[i:i + 16] for i in range(0, len(ct), 16)][::-1]
    nonce = blocks2[0] # = A

    blocks1 = [nonce]
    for i in range(len(blocks2) - 1):
        tmp = bytes(x ^ y for x, y in zip(blocks1[i], blocks2[i + 1]))
        blocks1 += [cipher.encrypt(tmp)]

    # A 
    # e(A ^ B) 
    # e(e(A ^ B) ^ C) 
    # e(e(e(A ^ B) ^ C) ^ D) 
    # e(e(e(e(A ^ B) ^ C) ^ D) ^ E)
    # e(e(e(e(e(A ^ B) ^ C) ^ D) ^ E) ^ F)
    # e(e(e(e(e(e(A ^ B) ^ C) ^ D) ^ E) ^ F) ^ G)
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
