#!/usr/bin/env python3

import os
from random import shuffle
from hashlib import sha256

flag = os.getenv('FLAG', 'CCIT{redacted}').encode()

class OTPgen:
    def __init__(self):
        self.s = os.urandom(32)
        self.i = 0
    
    def __iter__(self):
        while True:
            if self.i == len(self.s):
                self.s = sha256(self.s).digest()
                self.i = 0
            yield self.s[self.i]
            self.i += 1

    def __rxor__(self, other):

        return bytes([x^y for x,y in zip(self, other)])
    
    def __xor__(self, other):
        return other ^ self

N = len(flag)
perm = list(range(N))
shuffle(perm)
mask = OTPgen()

def enc(msg):
    out = bytes([msg[perm[i]] for i in range(N)])
    out ^= mask
    return out

while True:
    print('1) Encrypt a message')
    print('2) Get the encrypted flag')

    choice = input('> ')

    if choice == '1':
        pt = bytes.fromhex(input('Message (hex): ').strip())

        if len(pt) != N:
            print(':(')
            continue

        print(enc(pt).hex())

    elif choice == '2':
        print(enc(flag).hex())
    
    else:
        print('Bye!')
        break