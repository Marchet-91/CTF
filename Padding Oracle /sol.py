from pwn import *

def checkStream():
    print("cia")

def bruteForce(io, ct, pos):
    for i in range(16):
        tmp = ct[pos - 1][15 - i]
        for b in range(256):
            test = ct[:]
            block = test[pos - 1].copy()
            block[15 - i] = tmp ^ b ^ (i + 1)
            test[pos - 1] = block
            io.sendlineafter(b"? ", b"".join(test).hex().encode())
            if b"incorrect" not in io.recvline():
                print(i, b)
                break
        ct[pos - 1][15 - i] = tmp


    return 


HOST = "padding-oracle.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)

io.recvline()
ct = io.recvline().decode().strip()
ct = bytes.fromhex(ct)
ct = [bytearray(ct[i:i+16]) for i in range(0, len(ct), 16)]

# ct = [ct[i:i+16] for i in range(0, len(ct), 16)]
# print(len(ct))
for i in range(len(ct) - 1, 0, -1):
    # print("ciao")
    print(bruteForce(io, ct, i))
    break


# print(ct)

# for i in range(len(ct) - 1, 0, -16):


io.close()