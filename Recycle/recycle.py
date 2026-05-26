#!/usr/bin/env python3

from Crypto.Cipher import AES
import os
import math

flag = os.getenv("FLAG", "CCIT{redacted}")

flag = flag.encode()
key = os.urandom(16)
nonce = os.urandom(8)

cipher = AES.new(key, AES.MODE_CTR, nonce = nonce, initial_value = 0)
counter_value = 0

while True:
    print("What do you want to do?")
    print("1. Encrypt a block")
    print("2. Encrypt the flag")
    print("3. Change nonce")
    try:
        choice = int(input("> "))

        if choice == 3:
            nonce = bytes.fromhex(input("> ").strip())
        elif choice == 1:
            block = os.urandom(16)
            cipher = AES.new(key, AES.MODE_CTR, nonce = nonce, initial_value = counter_value)
            enc = cipher.encrypt(block)
            print(block.hex(), enc.hex())
            counter_value += 1
        elif choice == 2:
            cipher = AES.new(key, AES.MODE_CTR, nonce = nonce, initial_value = counter_value)
            enc = cipher.encrypt(flag)
            print(enc.hex())
            counter_value += math.ceil(len(flag)/16)
    except:
        print("Something went wrong")
        exit()