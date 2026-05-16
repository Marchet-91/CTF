from Crypto.Util.number import getPrime, GCD, bytes_to_long
from secret import FLAG

N_CC = 20
nbits = 1024

def getRSA(nbits, e=17):
    p, q = getPrime(nbits), getPrime(nbits)
    while GCD(p - 1, e) != 1 or GCD(q - 1, e) != 1:
        p, q = getPrime(nbits), getPrime(nbits)
    d = pow(e, -1, (p - 1) * (q - 1))
    return p * q, e, d


secret_keys = [getRSA(nbits) for _ in range(N_CC)]
public_keys = [(n, e) for n, e, _ in secret_keys]
data = [(n, e, pow(bytes_to_long(FLAG), e, n)) for n, e in public_keys]
with open("ciphertext.txt", "w") as f:
    f.write(f"{data = }")


# 