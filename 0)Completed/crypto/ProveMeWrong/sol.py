from operator import lshift
from random import SystemRandom
import math
from Crypto.Util.number import getPrime, isPrime, long_to_bytes, bytes_to_long

random = SystemRandom()
nbits = 256
srdnlen = b"we are srdnlen!"

def decode(e, p, q, N, ct):
    fi = (p-1)*(q-1)
    d = pow(e, -1, fi)
    pt = pow(ct, d, N)
    print(pt)
    print(long_to_bytes(pt))
    print(long_to_bytes(pt).decode())

somma = 0

n = 3939930432607568271028006178835273343365969273890011029334148059968112291984800526003772464130883943191723987350327352277647934827274472714706501384053753
e = 65537
flag_enc = 2869429344439206906531588120924725691313414493116437092996652346479439780409533002845413737504581129739595694725033319847726785183127845067606127237223702
sample = [18, 32, ..., ..., 130, 138, 145, ..., 180, 183, 189, 205, 221, ..., ...]


print("FInish")
for first in range(32, 131):
    for second in range(first, 131):
        for third in range(145,181):
            for fourth in range(221, 256):
                for fifth in range(fourth, 256):
                    # print(sample)
                    sample[2] = first
                    sample[3] = second
                    sample[7] = third
                    sample[-2] = fourth
                    sample[-1] = fifth
                    x = sum(map(lshift, srdnlen, sample))**2 + 4*n
                    if x < 0:
                        continue
                    radice = math.isqrt(x)
                    if radice**2 == x:
                        p = (-(sum(map(lshift, srdnlen, sample))) + radice) // 2
                        if p > 0:
                            print("Discriminante:", x)
                            print(sample)
                            q = p + sum(map(lshift, srdnlen, sample))
                            decode(e, p, q, n, flag_enc)
                        p = (-(sum(map(lshift, srdnlen, sample))) - radice) // 2
                        if p > 0:
                            print("Discriminante:", x)
                            print(sample)
                            q = p + sum(map(lshift, srdnlen, sample))
                            decode(e, p, q, n, flag_enc)