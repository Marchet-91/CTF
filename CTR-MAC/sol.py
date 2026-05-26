import sys, base64
from pwn import remote

host, port = "ctrmac.challs.cyberchallenge.it", 37003
admin = b'default_server_admin'

forged = bytearray(admin)
forged[0]  ^= 0x80          # flip top bit of block 0
forged[16] ^= 0x80          # flip top bit of block 1
forged = bytes(forged)

io = remote(host, port)

# 1) register the colliding username -> get a token
io.sendlineafter(b'> ', b'1')
# print(io.recvline())
io.sendlineafter(b'base64):', base64.b64encode(forged))
io.recvuntil(b'token: ')
token = io.recvline().strip().decode()

# 2) login AS admin using that same token
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'base64): ', base64.b64encode(admin))
io.sendlineafter(b'Token: ', token.encode())

io.recvall(timeout=5)  # flag printed after admin login
print(io.recvall(timeout=2).decode(errors='replace'))
io.close()