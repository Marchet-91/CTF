import string

OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]
ciphertext = "fegdeogdgecoeocgcgchcfcffccfca"

def shift(c, k):
    t1 = ord(c) - OFFSET
    t2 = ord(k) - OFFSET
    return ALPHABET[(t1 + t2) % len(ALPHABET)]

def b16_decode(ct):
    pt = ""
    for c in range(0, len(ct), 2):
        p1 = ALPHABET.index(ct[c])
        p2 = ALPHABET.index(ct[c+1])
        pt += chr((p1<<4) + p2)
    
    return pt

for k in string.ascii_lowercase:
    ct = ""
    for c in ciphertext:
        ct += shift(c, k)
    
    print(k,b16_decode(ct))