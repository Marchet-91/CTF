from pwn import * 

HOST = "crypto-08.challs.olicyber.it"
PORT = 30001

io = remote(HOST, PORT)

io.recvline()
io.recvline()
io.recvline()
quest = io.recv(4096)
while b"flag" not in quest:
    quest = quest.decode().split(" ")
    print(quest)
    first = int(quest[0]) % int(quest[2])
    io.sendline(str(first).encode())
    print(io.recvline())
    quest = io.recv(4096)


print(quest)

io.close()

# flag{t1ck_t0ck_M4th_1s_0n_th3_Cl0cK}