from pwn import * 

def bitxor(args):
    res = 0
    for arg in args:
        res = int(res) ^ int(arg)
    return res

def strxor(al, bl):
    res = []
    for a, b in zip(al, bl):
        res.append(chr(bitxor([a, b])))
    return res

HOST = "interdumpotp.chall.srdnlen.it"
PORT = 443
flag = ""

while "srdnlen" not in flag:
    io = remote(HOST, PORT,ssl=True)

    x0 = ("0"*16).encode()
    x1 = ("0"*15 + "1").encode()

    io.sendlineafter(b"Give me an x0: ", x0)
    io.sendlineafter(b"Give me an x1: ", x1)

    array = io.recvline().decode().strip().split(", ")
    array[0] = array[0][-16:]

    # print(strxor(x1, [1]*16)))

    ans = ""

    for i in array:
        if i == "0"*16 or i == "1"*16:
            ans += "0,"
        elif i == "1"*15 + "0":
            ans += "1,"
        else:
            ans += "1,"

    io.sendlineafter(b"Guess: ", ans[:-1].encode())
    flag = io.recvline().decode()

    io.close()

print(flag)