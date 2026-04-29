from pwn import *
from Crypto.Cipher import AES

def dump_user(user):
    def try_to_bytes(x):
        if type(x) == bytes:
            return x
        elif type(x) == str:
            return x.encode()
        else:
            return str(x).encode()
    return b"&".join(key.encode()+b"="+try_to_bytes(value) for key, value in user.items())

HOST = "cookieecb.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)

payload = b"AAAAAAAAAAAA&admin=True"

io.sendlineafter(b"Hello! What's your name? ", payload)

cookie = io.recvline()
print(cookie)

io.close()