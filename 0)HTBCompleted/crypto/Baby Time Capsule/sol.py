from pwn import * 
import json
from sage.all import *
from Crypto.Util.number import *
from gmpy2 import iroot

HOST = "154.57.164.61"
PORT = 31626

e = 5
Cs = []
Ns = []

io = remote(HOST, PORT)
for i in range(e):
    # io = remote(HOST, PORT)

    io.sendlineafter(b")", b"Y")
    diz = json.loads(io.recvline().decode())
    Cs.append(int(diz['time_capsule'],16))
    Ns.append(int(diz['pubkey'][0], 16))

io.close()

m_e = crt(Cs, Ns)
m = m_e.nth_root(e)
print(long_to_bytes(int(m)).decode())