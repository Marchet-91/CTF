from pwn import * 

HOST = "primerng.chall.srdnlen.it"
PORT = 443
ROUNDS = 32
TRIES = 32

io = remote(HOST, PORT, ssl=True)

# print(io.recvline())
# print(io.recvline())
# print(io.recvline())
for i in range(ROUNDS):
    print(i)
    for j in range(TRIES):
        # print(j)
        if j == 0:
            io.sendlineafter(b">>> ", b"0")
        else:
            io.sendlineafter(b">>> ", str(j * 2 ** 1337).encode())
        resp = io.recvline()
        if b"earned" in resp:
            break
    # print(io.recvline())

print(io.recvline())
print(io.recvline())
# print(io.recvline())

io.close()