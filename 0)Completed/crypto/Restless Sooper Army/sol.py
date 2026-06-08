from pwn import * 
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from string import printable

def searchKey(ctKey, d, n):
    # c = int.from_bytes(ctKey, byteorder='big')
    c = pow(ctKey, d, n)
    back = c.to_bytes((c.bit_length() + 7) // 8, "big")
    return back


HOST = "rsa.challs.olicyber.it"
PORT = 10300

io = remote(HOST, PORT)

io.recvuntil(b"(p): ")
p = int(io.recvline().decode().strip())
q = int(io.recvline().decode().strip().split(" ")[-1])
e = int(io.recvline().decode().strip().split(" ")[-1])

n = p * q
fi = (p - 1) * (q - 1)
d = pow(e, -1, fi)
io.sendlineafter(b"(n): ", str(n).encode())
io.sendlineafter(b"(n): ", str(fi).encode())
io.sendlineafter(b"(d): ", str(d).encode())

pt = io.recvuntil(b": ").split(b"'")[1]
pt = bytes_to_long(pt)
ct = pow(pt, e, n)

io.sendline(str(ct).encode())
# io.interactive()
io.recvuntil(b"challenge.\n")


iv = bytes.fromhex(io.recvline().strip().decode().split(" ")[-1])
chiave = io.recvline().strip().decode().split(" ")[-1]
# print(chiave.encode())
chiave = int(chiave, 16)
token = bytes.fromhex(io.recvline().strip().decode().split(" ")[-1])

key = searchKey(chiave, d, n)

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(token), 16)
print(plaintext.decode())

# print(chiave)
