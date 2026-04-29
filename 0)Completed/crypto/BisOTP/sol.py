from pwn import *

HOST = "bisotp.chall.srdnlen.it"
PORT = 443
SIZE = 16

io = remote(HOST, PORT, ssl=True)

x0 = ("0"*16).encode()
x1 = ("0"*15 + "1").encode()

io.sendlineafter(b"Give me an x0: ", x0)
io.sendlineafter(b"Give me an x1: ", x1)

array = io.recvline().decode().strip().split(", ")
array[0] = array[0][-16:]

ans = ""
for i in array:
    if i[:SIZE // 2] == i[SIZE // 2:]:
        ans += "0,"
    else:
        ans += "1,"

io.sendlineafter(b"Guess: ", ans[:-1].encode())
print(io.recvline())

io.close()