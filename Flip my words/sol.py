import json
from pwn import *
from base64 import b64encode, b64decode

io = remote("flip.challs.olicyber.it", 10603)
# io = process(["python3", "source.py"])

plaintext = json.dumps({'admin': False, 'msg': "Dammi la flaaag!"}).encode()
first = plaintext[:16]
pt = "Dammi la flaaag!".encode()

io.sendlineafter(b"!!!", b"1")
io.sendlineafter(b": ", pt)

ct = b64decode(io.recvline().split(b" ")[-1].decode().strip())
iv = b64decode(io.recvline().split(b" ")[-1].decode().strip())
new_pt = b'{"admin": true ,'
# print(first.decode())

forge_iv = b64encode(xor(xor(iv, first), new_pt))
io.sendlineafter(b"!!!", b"2")
# print(b64encode(ct))
# print(forge_iv)
# io.interactive()
io.sendlineafter(b": ", b64encode(ct))
# io.interactive()
io.sendlineafter(b": ", forge_iv)
io.recvline()
io.recvline()
io.recvline()
print(io.recvline())

io.sendlineafter(b"!!!", b"3")

io.close()
