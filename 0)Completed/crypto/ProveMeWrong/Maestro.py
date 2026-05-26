import gmpy2
from tqdm import tqdm
from Crypto.Util.number import long_to_bytes

nbits = 256
srdnlen = b"we are srdnlen!"

with open("output.txt", "r") as f:
    n = int(f.readline().strip().lstrip("n = "))
    e = int(f.readline().strip().lstrip("e = "))
    flag_enc = int(f.readline().strip().lstrip("flag_enc = "))
    f.readline()
    leaked_sample = f.readline().lstrip("sample = [").rstrip("]\n")
    leaked_sample = [int(element) if element != "..." else None for element in leaked_sample.split(", ")]


def find_next_top(i):
    global nbits, leaked_sample
    for j in range(i, len(leaked_sample)):
        if leaked_sample[j] is not None:
            return leaked_sample[j]
    return nbits


factored = False
p, q = None, None
def combinations(base, top, i, coefficient):
    global factored, srdnlen, leaked_sample, n, p, q

    if i == len(leaked_sample):
        root = (-coefficient + int(gmpy2.isqrt(coefficient ** 2 + 4 * n))) // 2
        if 0 < root < n and n % root == 0:
            p, q = root, n // root
            factored = True
        return

    next_top = find_next_top(i + 1)
    if leaked_sample[i] is not None:
        combinations(leaked_sample[i] + 1, next_top, i + 1, coefficient + (srdnlen[i] << leaked_sample[i]))
        return

    for element_guess in (tqdm(range(base, top)) if i == leaked_sample.index(None) else range(base, top)):
        if factored:
            return
        combinations(element_guess + 1, next_top, i + 1, coefficient + (srdnlen[i] << element_guess))


combinations(0, find_next_top(0), 0, 0)
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
print(long_to_bytes(pow(flag_enc, d, n)).decode())
