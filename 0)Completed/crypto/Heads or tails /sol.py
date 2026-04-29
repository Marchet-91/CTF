from pwn import * 

HOST = "heads-or-tails.chall.srdnlen.it"
PORT = 443

HEAD = "headsVLK"
TAIL = "tailsAEB"

io = remote(HOST, PORT, ssl=True)

io.recvuntil(b"> ")
io.sendline(b"1")
for i in range(100):
    io.sendlineafter(b"\n", b"0oO0OOoOoO0oo000oOOOo")
    text = io.recvuntil(b"\n").decode().strip().split(" ")[6]
    if text == "heads":
        io.sendline(HEAD.encode())
    else:
        io.sendline(TAIL.encode())
    io.recvline()
print(io.recvline().decode())




io.close()