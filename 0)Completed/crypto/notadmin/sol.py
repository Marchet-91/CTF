from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
from Crypto.Cipher import AES
from pwn import * 

key = os.urandom(16)

def enc(cookie):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(cookie, 16))
    return iv.hex() + encrypted.hex()

def dec(token):
    cookie = bytes.fromhex(token[32:])
    iv = bytes.fromhex(token[:32])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print("sol1: ", cookie)
    # print("sol2: ", cipher.decrypt(cookie))
    pt = unpad(cipher.decrypt(cookie),16)
    values = pt.split(b";")
    user = values[0].split(b"=")[-1]
    return pt


HOST = "notadmin.challs.cyberchallenge.it"
PORT = 9032

io = remote(HOST, PORT)

name = ""
pt = f"usr={name};is_admin=0".encode()
my = b'usr=;is_admin=1\x01'
# # sblock = c
# print(c[:16])
# print(c[16:32])
# print(pad(c[32:], AES.block_size))


io.sendlineafter(b"> ", b"1")
io.sendlineafter(b": ", name.encode())
# cookie = enc(pt)

cookie = io.recvline().strip().split(b" ")[-1]
cookie = bytes.fromhex(cookie.decode())
# print(len(cookie))

iv = cookie[:16]
a = cookie[16:]
# print(cookie)
# print(iv, a)
# print(chr(pt[-1]))
# print(chr(c[-1]))
# print(iv)
# print(iv[:-2], iv[-1:])
new = strxor(strxor(iv, pad(pt, AES.block_size)), my) 
# print("n: ", new)
# print(iv + a + new + c)
# print(cookie)

# print(dec((new).hex() + (a).hex()))

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b": ",((new).hex() + (a).hex()).encode())
print(io.recvline())
print(io.recvline())

io.close()