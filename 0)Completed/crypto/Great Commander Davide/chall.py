from Crypto.Util.number import getPrime, bytes_to_long
from random import randrange

n = 5
nbits = 1024

e = 65537

p = [getPrime(nbits) for _ in range(n)]
q = [getPrime(nbits) for _ in range(n)]

def encrypt(plain):
    P = p[randrange(0, n)]
    Q = q[randrange(0, n)]

    M = bytes_to_long(plain.encode())

    C = pow(M, e, P*Q)
    return C, P*Q


if __name__ == '__main__':
    pt = open('plain.txt', 'r').read().split("\n")
    ct = open('cipher.txt', 'w')
    for plain in pt:
        enc, N = encrypt(plain)
        ct.write(f"enc: {enc} N: {N}\n")
    ct.close()