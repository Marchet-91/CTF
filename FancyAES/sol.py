from pwn import *

HOST = "fancyaes.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)



io.close()