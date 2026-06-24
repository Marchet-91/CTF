from pwn import * 
from factordb.factordb import FactorDB
from Crypto.Util.number import long_to_bytes

HOST = "verbal-sleep.picoctf.net"
PORT = 65130

io = remote(HOST, PORT)

n = int(io.recvline().strip().split(b": ")[1].strip())
e = int(io.recvline().strip().split(b": ")[1].strip())
ct = int(io.recvline().strip().split(b": ")[1].strip())

io.close()

# print(n)
f = FactorDB(n)
f.connect()

p,q = 2, n // 2
fi = (p-1)*(q-1)
d = pow(e, -1, fi)
print(long_to_bytes(pow(ct, d, n)).decode())


