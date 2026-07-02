from pwn import * 


# io = remote("cryptorland.challs.olicyber.it", 10801)
context.log_level ="error"

result = b"Nope!"

while b"Nope" in result:
    io = remote("cryptorland.challs.olicyber.it", 10801)
    num = []
    for i in range(10):
        n = int(io.recvline().strip().decode())
        # print(n)
        num.append(bin(n)[2:].rjust(96, '0'))
        # print(int(num[i], 2))


    secret = ""
    for i in range(96):
        one = 0
        zero = 0
        for b in num: 
            if b[i] == '1':
                one += 1
            else:
                zero += 1
            
        if one > 6: 
            secret += '1'
        else: 
            secret += '0'
    
    io.sendlineafter(b"? ", str(int(secret, 2)).encode())
    result = io.recvline()
    # print(result)
    io.close()

print(result.decode().strip().split(" ")[-1])