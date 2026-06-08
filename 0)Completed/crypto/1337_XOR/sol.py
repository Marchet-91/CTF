import os
import string
from pwn import *

def vigenere_attack(ct, key):
    for i in range(256): 
        tmp = key + bytes([i])
        if i == 182:
            print(xor(tmp,ct).decode())

ct = bytes.fromhex(open("output.txt", "r").read().split()[-1])

key = xor(b"flag{", ct[:5])
# print(len(key))

vigenere_attack(ct, key)
