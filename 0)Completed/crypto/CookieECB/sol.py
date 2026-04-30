from pwn import * 
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from scheme import decrypt, encrypt

HOST = "cookieecb.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)

def dump_user(user):
    def try_to_bytes(x):
        if type(x) == bytes:
            return x
        elif type(x) == str:
            return x.encode()
        else:
            return str(x).encode()
    return b"&".join(key.encode()+b"="+try_to_bytes(value) for key, value in user.items())

payload = b"AAAAAAA"
block = pad(b"True", AES.block_size)
sequel = b"AAAAAAAAA"

user = {"username": payload+block+sequel, "admin": b"False"}
ct = dump_user(user)

io.sendlineafter(b"Hello! What's your name? ", payload + block + sequel)
io.recvuntil(b"! ")
cookie = io.recvline().decode().strip()
# cookie = bytes.fromhex(cookie)

# cookie[-16:] = cookie[16:32]
right = cookie[:-16*2] + cookie[16*2:16*4]

# print(cookie)
io.sendlineafter(b"? ", right.encode())
print(io.recvline())
# print(result)

io.close()