from pwn import * 

HOST = ""
PORT = 0

io = remote(HOST, PORT)

nums = []
for 