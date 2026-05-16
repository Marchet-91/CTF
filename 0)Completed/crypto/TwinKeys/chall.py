from Crypto.Util.number import getPrime, GCD, bytes_to_long
from secret import FLAG

e0, e1 = 0x1337, 0x10001

p, q = getPrime(2048), getPrime(2048)
while GCD(e0, (p - 1) * (q - 1)) != 1 and GCD(e1, (p - 1) * (q - 1)) != 1:
    p, q = getPrime(2048), getPrime(2048)
n = p * q

ct0, ct1 = pow(bytes_to_long(FLAG), e0, n), pow(bytes_to_long(FLAG), e1, n)

with open("ciphertext.txt", "w") as f:
    f.write(f"{n = }\n")
    f.write(f"{e0 = }\n")
    f.write(f"{ct0 = }\n")
    f.write(f"{e1 = }\n")
    f.write(f"{ct1 = }\n")
