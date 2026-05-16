from Crypto.Util.number import long_to_bytes
from math import gcd

e = 65537

def decrypt(n1, n2, ct1, ct2):
    p1, q1 = gcd(n1, n2), n1 // gcd(n1, n2) 
    p2, q2 = gcd(n1, n2), n2 // gcd(n1, n2)
    print(n1 // gcd(n1, n2))

    f1, f2 = (p1 - 1)*(q1 - 1), (p2 - 1)*(q2 - 1)

    # print(f1, f2)
    d1, d2 = pow(e, -1, f1), pow(e, -1, f2)

    return long_to_bytes(pow(ct1, d1, n1)).decode(), long_to_bytes(pow(ct2, d2, n2)).decode()

txt = open('cipher.txt', 'r').read().split("\n")

N = []
CT = []
for c in txt:
    CT.append(int(c.split(" ")[1]))
    N.append(int(c.split(" ")[-1]))

# print(N)

for i, n1 in enumerate(N):
    for j in range(i + 1, len(N), 1):
        if gcd(n1, N[j]) != 1 and n1 != N[j]:
            # if n1 == N[j] and n1 != N[j]:
            print(decrypt(n1, N[j], CT[i], CT[j]))