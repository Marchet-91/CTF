from hashlib import sha256
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Random import get_random_bytes
import os
from Crypto.Util.strxor import strxor

def mixkeybit(keybit1, keybit2, keybit3):
    return int(keybit1 or (not(keybit2) and keybit3))

flag = "srdnlen{fchvauifwodv}"

# flagbin = bytes_to_long(flag.encode())
# print(flagbin)

with open("output.txt", "r") as f:
    ct = f.readline()



for i in range(2):
    for j in range(2):
        for k in range(2):
            pt = ""
            for c in range(len(ct)):
                pt += str(mixkeybit(i, j, k) ^ int(ct[i])) 
            pt = int(pt, 2)
            pt = long_to_bytes(pt)
            print(pt)
            print(i,j,k)

