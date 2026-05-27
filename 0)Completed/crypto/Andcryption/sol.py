from pwn import * 
from hashlib import sha256

#nc 10.100.0.2 30492
HOST = "10.100.0.2"
PORT = 30492

io = remote(HOST, PORT)

i = -1
flag = b"\x00" * 32
while True:
    i += 1
    tmp = b""
    io.sendlineafter(b"? ", str(i).encode())
    k = bytes.fromhex(io.recvline().strip().decode().split(" ")[-1])
    # print(len(flag),len(k))
    for f, c in zip(flag, k):
        # print(bin(f), bin(c))
        # print(int(bin(f), 2), int(bin(c), 2))
        # print(bin(int(bin(f), 2) | int(bin(c), 2)))
        c = (int(bin(f), 2) | int(bin(c), 2))
        tmp += c.to_bytes()

    flag = tmp
    print(flag)
    # flag = tmp
    # print(flag)

# io.close()