from hashlib import sha256
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Random import get_random_bytes
import os
from Crypto.Util.strxor import strxor

def mixkeybit(keybit1, keybit2, keybit3):
    return int(keybit1 or (not(keybit2) and keybit3))

# flagbin = bytes_to_long(flag.encode())
# print(flagbin)

with open("output.txt", "r") as f:
    ct = f.readlines()
    flagCt = []
    for c in ct:
        flagCt += [c.strip()]
    ct = flagCt

key = ""

for i in range(len(ct[0])):
    diz = {"0":  1, "1": 0}
    for j in ct:
        diz[j[i]] += 1
    if diz["0"] > diz["1"]:
        key += "0"
    else:
        key += "1"

# print(key)

conta = 0
for lines in ct:
    flag = ""
    for i in range(len(key)):
        flag += str(int(key[i]) ^ int(lines[i]))
    num = int(flag, 2)
    num = long_to_bytes(num)
    # print(num)
    try:
        print(num.decode())
    except UnicodeDecodeError:
        conta += 1
        # print("non funziona")

for i in range(2):
    for j in range(2):
        for k in range(2):
            for t in range(2):
                print(i,j,k,t,"    " ,mixkeybit(i,j,k) ^ t)

print(conta)
# print(key)