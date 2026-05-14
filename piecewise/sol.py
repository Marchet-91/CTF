from pwn import * 

HOST = "piecewise.challs.cyberchallenge.it"
PORT = 9110

def doing(n, d, t):
    if "32" in d:
        if "little" in t:
            return p32(n, endianness='little',sign="unsigned")[::-1]
        else:
            return p32(n, endianness='big',sign="unsigned")[::-1]
    elif "64" in d:
        if "little" in t:
            return p64(n, endianness='little', sign="unsigned")[::-1]
        else:
            return p64(n, endianness="big",sign="unsigned")[::-1]
    else:
        exit()

io = remote(HOST, PORT)

flag = ""
First = True
i = 0
while flag == "" or flag[-1] != '}': 
    i += 1
    print("Tipo: ", i)
    txt = io.recvline(timeout=1)
    print(txt)
    if b"flag" in txt:
        flag += txt.strip().decode().split()[-1][-1]
        print(flag)
        continue
    if b"Please send me an empty line (that is, just the byte 10)\n" in txt:
        io.send(b"\n")
        continue
    number = int(txt.strip().decode().split(" ")[5])
    dim = txt.strip().decode().split(" ")[8]
    tipo = txt.strip().decode().split(" ")[9]
    print(number, dim, tipo)
    print(type(doing(number, dim, tipo)))
    io.sendline(doing(number, dim, tipo))
    # io.interactive()
    # io.recvline()
    # io.sendlineafter(b")", bytes(10))
    First = False
    # print(io.recvline())

io.close()