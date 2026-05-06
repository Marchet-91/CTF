from pwn import * 
from Crypto.Cipher import DES, AES, ChaCha20
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

HOST = "crypto-07.challs.olicyber.it"
PORT = 30000

def encrypt(method, mode, iv, keyHex, pt, padding):
    if b"DES" in method:
        if b"CBC" in mode:
            crypt = DES.new(bytes.fromhex(keyHex), DES.MODE_CBC, iv)
            if b"x923" in padding:
                pt = pad(pt.encode(), 8, style="x923")
            else:
                print(padding)
        else:
            print(mode)
    elif b"AES256" in method:
        if b"CFB" in mode:
            crypt = AES.new(keyHex, AES.MODE_CFB, iv,segment_size=24)
            if b"pkcs7" in padding:
                pt = pad(pt.encode(), 16)
            else:
                print(padding)
        else:
            print(mode)
    
    ct = crypt.encrypt(pt)
    return ct

def decrypt(method, keyHex, ct, nonce):
    ct = bytes.fromhex(ct)
    if b"ChaCha20" in method:
        dec = ChaCha20.new(key=bytes.fromhex(keyHex), nonce=bytes.fromhex(nonce))
    
    return dec.decrypt(ct)

io = remote(HOST, PORT)
io.recvline()
io.recvline()
io.recvline()
# print(io.recvline())

iv = get_random_bytes(8)
cipher = io.recvline()
# print(cipher)
mode = io.recvline()
keyHex = io.recvline().decode().split("'")[-2]
# print(keyHex)
pt = io.recvline().decode().split("'")[-2]
padding = io.recvline()
ct = encrypt(cipher,mode, iv, keyHex,pt, padding)

io.sendlineafter(b"? ", ct.hex().encode())
io.sendlineafter(b"? ", iv.hex().encode())

io.recvline()
io.recvline()
io.recvline()

iv = get_random_bytes(16)
method = io.recvline()
if b"256" in method:
    key = get_random_bytes(32)
mode = io.recvline()
pt = io.recvline().decode().split("'")[-2]
padding = io.recvline()
size = io.recvline()
ct = encrypt(method, mode, iv, key, pt, padding)

io.sendlineafter(b"? ", key.hex().encode())
io.sendlineafter(b"? ", ct.hex().encode())
io.sendlineafter(b"? ", iv.hex().encode())

io.recvline()
io.recvline()
io.recvline()
io.recvline()

method = io.recvline()
keyHex = io.recvline().decode().split("'")[-2]
ct = io.recvline().decode().split("'")[-2]
nonceHex = io.recvline().decode().split("'")[-2]

pt = decrypt(method, keyHex, ct, nonceHex)
# print(pt)
io.sendlineafter(b"? ", pt)
io.recvline()
io.recvline()

print(io.recvline())
# io.interactive()

io.close()