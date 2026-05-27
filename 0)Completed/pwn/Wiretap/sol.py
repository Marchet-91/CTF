#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
# from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './wiretap')
# lib = CDLL(exe.libc.path)
host = args.HOST or '10.100.0.2'
port = int(args.PORT or 38076)

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
b *main+75
continue
'''.format(**locals())


# -- Exploit goes here --

def checksum(a):
    s = 0
    for i in a:
        s += ord(i)
    print(s)

io = start()
h = b"\x7f\x43\x43\x07"
c1 = 5
p = b"GETFLAG"
c = b"\x06"
io.send(h)
io.send(p)
io.send(c)
print(io.recvline().decode())

io.close()

