import os
import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64decode, b64encode
from pwn import * 
from string import printable

k1 = os.urandom(32)
nonce = os.urandom(8)

def compress(l):
    l = [l[i:i+16] for i in range(0,len(l),16)]
    l = [int.from_bytes(l_, 'big') for l_ in l]
    return (sum(l) & (2**128 - 1)).to_bytes(16, 'big')

def sign(data):
    cipher = AES.new(k1, AES.MODE_CTR, nonce=nonce)
    enc_data = cipher.encrypt(pad(data, 16))
    compressed = compress(enc_data)
    return compressed

HOST = "ctrmac.challs.cyberchallenge.it"
PORT = 37003

my = sign(b"ciao")

print(bin(2**128 - 1))

# io = remote(HOST, PORT)


# io.sendlineafter(b"")

# io.close()