from pwn import *
from randcrack import RandCrack

HOST = "fixedmersenne.chall.srdnlen.it"
PORT = 443
TRIES = 1337 % 1000
BIT = 624 * 8 - 1

io = remote(HOST, PORT, ssl=True)

rd = RandCrack()

io.recvuntil(b":\n")
for _ in range(4):
    line = io.recvline().decode()
    num = int(''.join(c for c in line if c.isdigit()))
    words = []
    for i in range(156):
        words.append(num & 0xffffffff)
        num >>= 32

    for w in reversed(words):
        rd.submit(w)

# num = rd.predict_getrandbits(BIT)
# print(num)
for i in range(TRIES):
    guess_words = [rd.predict_getrandbits(32) for _ in range(156)]

    guess = 0
    for j, w in enumerate(guess_words):
        guess |= (w << (32 * j))

    io.sendlineafter(b">>> ", str(guess))
    print(i, io.recvline())

print(len(rd.mt))

io.close()