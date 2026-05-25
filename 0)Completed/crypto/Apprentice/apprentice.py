#!/usr/bin/env python3
from Crypto.Hash import SHA3_384

def enc(plain):
    res = b''
    for c in plain:
        res += SHA3_384.new(bytes([c])).digest()[:2]
    return res.hex()

if __name__ == '__main__':
    with open('flag.txt', 'rb') as rf:
        flag = rf.read().strip()
        
    print(enc(flag))

