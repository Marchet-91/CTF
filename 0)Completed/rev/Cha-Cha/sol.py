from pwn import * 
from string import printable

io = process(["./cha-cha", ""])
context.log_level = 'error'

flag = ""
first = True
while first or flag[-1] != "}":
    first = False
    for c in printable:
        io = process(["./cha-cha", flag+c])
        resp = io.recvline()
        if b"You got it!" in resp:
            flag += c
            print(flag)
            break
        io.close()
        # print(resp)

io.close()