from Crypto.Hash import SHA3_384
from string import printable

with open("apprentice_output.txt", "r") as f:
    ct = f.readline().strip()

ct = bytes.fromhex(ct)

pt = ""
for i in range(0, len(ct), 2):
    for c in printable:
        test = SHA3_384.new(bytes(c.encode())).digest()[:2]
        # print(test, ct[i:i+2])
        if test == ct[i:i+2]:
            pt += c 
            break

print(pt)