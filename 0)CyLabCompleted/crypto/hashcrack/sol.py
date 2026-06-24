from pwn import *
from hashlib import md5, sha1, sha256
from string import printable

HOST = "verbal-sleep.picoctf.net"
PORT = 58787

io = remote(HOST, PORT)

# io.recvuntil(b": ")
# io.interactive()
h = io.recvline().decode().strip()
rock = open("/usr/share/wordlist/rockyou.txt", "rb").readlines()
# print(rock)

cache = {}
for i in range(3):
    io.recvuntil(b": ")
    h = io.recvline().decode().strip()
    
    if cache.get(h, 0) != 0:
        sol = cache[h]
        io.sendlineafter(b": ", sol.strip())
        continue

    for c in rock: 
        # print(c)
        if len(h) == 40:
            # print("sha1")
            test = sha1(c.strip()).hexdigest() 
        elif len(h) == 64:
            test = sha256(c.strip()).hexdigest() 
        else:
            test = md5(c.strip()).hexdigest() 
        if test == h:
            print(h, test)
            sol = c
            break
        
        if cache.get(h, 0) == 0:
            cache[test] = c

    io.sendlineafter(b": ", sol.strip())


# io.sendlineafter(b": ", c.strip())
io.interactive()