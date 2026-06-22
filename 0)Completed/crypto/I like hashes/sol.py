from string import printable
from hashlib import sha256

ct = open("ct.txt", "r").readlines()

cache = {}
pt = ""
for c in ct:
    if cache.get(c, 0) != 0: 
        pt += cache[c]
        continue
    for test in printable:
        h = sha256(test.encode()).digest().hex()
        
        if cache.get(h, 0) == 0:
            cache[h] = test
        
        if h == c.strip():
            pt += test

print(pt)