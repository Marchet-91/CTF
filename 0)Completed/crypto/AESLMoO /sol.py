import signal
import os
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from pwn import * 

key = os.urandom(32)


class AES_PCBC():
    def __init__(self, key: bytes):
        """Implementation of AES PCBC mode of operation"""
        self.key = key
    
    def encrypt(self, pt: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = pad(pt, AES.block_size)
        iv = os.urandom(AES.block_size)
        xor_block = iv

        ct = []
        for i in range(len(pt) // AES.block_size):

            ct.append(cipher.encrypt(strxor(pt[i * 16:(i + 1) * 16], xor_block)))
            xor_block = strxor(pt[i * 16:(i + 1) * 16], ct[i])

        ct = b"".join(ct)

        return (iv + ct).hex()
    
    def decrypt(self, iv: bytes, ct: bytes) -> bytes:
        assert len(iv) == AES.block_size, f"iv length must be {AES.block_size}"
        assert len(ct) % AES.block_size == 0, f"ct length must be multiple of {AES.block_size}"
        cipher = AES.new(self.key, AES.MODE_ECB)
        xor_block = iv

        pt = []
        for i in range(len(ct) // AES.block_size):
            
            pt.append(strxor(cipher.decrypt(ct[i * 16:(i + 1) * 16]), xor_block))
            xor_block = strxor(ct[i * 16:(i + 1) * 16], pt[i])

        pt = unpad(b"".join(pt), AES.block_size)

        return pt.hex()

io = remote("aeslmoo.chall.srdnlen.it", 443, ssl=True)

A = b"A"*15
plaintext = pad(b"admin", AES.block_size)
pt = A


# cookie = AES_PCBC(key).encrypt(pt)
# cookie = cookie[:64] + cookie[-64:]
# cookie = bytes.fromhex(cookie)
# iv = cookie[:16]
# iv_mio = strxor(strxor(iv, pad(pt, AES.block_size)), plaintext)
# cookie[:16] = iv_mio
# new_cookie = iv_mio + cookie[16:]
# username = bytes.fromhex(AES_PCBC(key).decrypt(new_cookie[:AES.block_size], new_cookie[AES.block_size:]))
# print(username)

io.sendlineafter(b">>> ", b"1")
io.sendlineafter(b") ", pt.hex().encode())
ct = io.recvline().strip()
ct = ct.split(b" ")[-1]
ct = bytes.fromhex(ct.decode())
iv = ct[:16]
iv_mio = strxor(strxor(iv, pad(pt, AES.block_size)), plaintext)
# cookie[:16] = iv_mio
new_cookie = iv_mio + ct[16:]
# print(ct)

io.sendlineafter(b">>> ", b"2")
io.sendlineafter(b") ", new_cookie.hex().encode())
print(io.recvline())
print(io.recvline())
print(io.recvline())

# print(pt)

io.close()