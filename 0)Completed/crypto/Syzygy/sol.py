from pwn import * 
import os
from random import shuffle
from hashlib import sha256

HOST = "10.100.0.2"
PORT = 40832

class OTPgen:
    def __init__(self):
        print("init")
        self.s = os.urandom(32)
        print(self.s)
        self.i = 0
    
    def __iter__(self):
        print("iter")
        while True:
            if self.i == len(self.s):
                self.s = sha256(self.s).digest()
                self.i = 0
            yield self.s[self.i]
            print(self.s)
            print((self.s[self.i]).to_bytes())
            self.i += 1

    def __rxor__(self, other):
        print(len(other))
        [print((x).to_bytes(),z) for x,z in zip(self, other)]
        return bytes([x^y for x,y in zip(self, other)])
    
    def __xor__(self, other):
        print("xor")
        return other ^ self


# def enc(msg):
#     out = bytes([msg[perm[i]] for i in range(N)])
#     out ^= mask
#     return out

def find_hash(pt, ct):
    h = bytes([x^y for x,y in zip(ct, pt)])
    return h

def findchar(c, pt):
    for i in range(len(pt)):
        # print(c, pt[i])
        if c == pt[i]:
            # print(c, pt[i], i)
            return i

io = remote(HOST, PORT)

payload = (b"A"*53)
payloadB = b"abcdefghijklmnopqrstuvwxyzABCDEFGIHJKLMNOPQRSTUVWXYZ\n"
# print(len(payloadB))
# print(payload)
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b": ", payload.hex().encode())
cta = bytes.fromhex(io.recvline().strip().decode())
a = find_hash(bytes.fromhex(payload[:32].hex()), cta[:32])
b = sha256(a).digest()
c = sha256(b).digest()
d = sha256(c).digest()
e = sha256(d).digest()
f = sha256(e).digest()

io.sendlineafter(b"> ", b"1")
io.sendlineafter(b": ", payloadB.hex().encode())
ctb = bytes.fromhex(io.recvline().strip().decode())

k = b[53-32:] + c[:53-11] + d[:10]
# print(53-32)
b = bytes([x^y for x,y in zip(ctb, k)])

perm = []
print(b)
print(payloadB)
for c in b:
    perm += [findchar(c, payloadB)]
print(perm)

newk = d[10:] + e + f[:10]

io.sendlineafter(b"> ", b"2")
ct = bytes.fromhex(io.recvline().strip().decode())

pt_d = "".join([chr(x^y) for x,y in zip(ct, newk)])
# print(pt_d)

pt = [" "]*53

for i in range(53):
    for pos, c in zip(perm,pt_d):
        if i == pos:
            print(c, end="")


print("\n")


io.close()