from operator import lshift
from random import SystemRandom
from Crypto.Util.number import getPrime, isPrime, long_to_bytes, bytes_to_long
from secret import flag

random = SystemRandom()
nbits = 256
srdnlen = b"we are srdnlen!"
assert isinstance(flag, bytes) and bytes_to_long(flag).bit_length() < 2 * nbits


class RSA():
    def __init__(self, nbits: int):
        self.p = getPrime(nbits)
        self.q = 0
        while not isPrime(self.q) or self.q.bit_length() != nbits:
            self.sample = sorted(random.sample(range(nbits), k=len(srdnlen)))
            self.q = self.p + sum(map(lshift, srdnlen, self.sample))

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 0x10001
        self.d = pow(self.e, -1, self.phi)
    
    def encrypt(self, pt: int) -> int:
        return pow(pt, self.e, self.n)

    def decrypt(self, ct: int) -> int:
        return pow(ct, self.d, self.n)


def leakage(sample: list) -> str:
    leaked_elements = sorted(random.sample(sample, k=round(len(sample) * 0.666)))
    return "[" + ", ".join(str(element) if element in leaked_elements else "..." for element in sample) + "]"


if __name__ == "__main__":
    rsa = RSA(nbits)
    flag_enc = rsa.encrypt(bytes_to_long(flag))
    assert rsa.decrypt(flag_enc) == bytes_to_long(flag)

    with open("output.txt", "w") as f:
        f.write(f"n = {rsa.n}\n")
        f.write(f"e = {rsa.e}\n")
        f.write(f"flag_enc = {flag_enc}\n")
        f.write(f"Oh no, there's a leakage, stacc@h stacc@h...\n")
        f.write(f"sample = {leakage(rsa.sample)}\n")
