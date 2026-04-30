#!/bin/env python3

import signal
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
import os
import string
TIMEOUT = 300

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("CCIT{"))
assert(FLAG.endswith("}"))

otp = os.urandom(8)

menu = """What do you want to do?

1. Encrypt text
2. Encrypt flag
0. Exit
"""

def xor(a, b):
    return bytes([a[i % len(a)] ^ b[i % len(b)] for i in range(max(len(a), len(b)))])

def encrypt_3des(text, key):
    try:
        key = bytes.fromhex(key)
        text = xor(bytes.fromhex(text), otp)
        cipher = DES3.new(key, DES3.MODE_ECB)
        ct = xor(cipher.encrypt(pad(text, 8)), otp)
        return ct.hex()
    except Exception as e:
        return f"Something went wrong: {e}"


def handle():
    while True:
        print("")
        print(menu)
        choice = input("> ").strip()
        if choice == "1":
            text = input("What do you want to encrypt (in hex)? ").strip()
            key = input("With what key (in hex)? ").strip()
            assert all(c in string.hexdigits for c in text)
            assert all(c in string.hexdigits for c in key)
            assert len(key) == 48
            print(encrypt_3des(text, key))
        elif choice == "2":
            key = input("What key do you want to use (in hex)? ").strip()
            assert all(c in string.hexdigits for c in key)
            print(encrypt_3des(FLAG.encode().hex(), key))
        else:
            return



if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
