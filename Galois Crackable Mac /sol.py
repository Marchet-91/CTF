from pwn import *

# context.log_level = 'error'

HOST = "gcm.chall.srdnlen.it"
PORT = 443
SECRET_STRING = b"VerySecretString".hex().encode()

io = remote(HOST, PORT, ssl=True)
        
# INPUT iniziale
io.sendlineafter(b"2) Guess my secret", b"1")
io.sendlineafter(b"Plaintext (hex): ", SECRET_STRING)
# print("ciao")
io.sendlineafter(b"2) MAC", b"2")
io.recvline()
io.recvline()
print(io.recvline())


io.close()
