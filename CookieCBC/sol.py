#!/usr/bin/env python3
from binascii import hexlify, unhexlify
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from pwn import *

# Constants
BLOCK_SIZE = 16
MAX_BYTE_VALUE = 255
HOST = "cookiecbc.chall.srdnlen.it"
PORT = 443

def compute_next_valid_iv_byte(keystream, padding, modified_iv):
    for i in range(len(keystream)):
        next_iv = keystream[i] ^ padding
        modified_iv[len(modified_iv)-1-i] = next_iv
    return modified_iv


def oracle_padding(original_iv, cookies, pt):
    keystream = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    plaintext = []

    # original_iv = original_ct[-96:-80]
    # cookies = original_ct[-80:-64]
    # print(original_iv)
    # print(cookies)

    modified_iv = bytearray(b'0000000000000000')
    padding = 0x01
    ks_index = 0
    for iv_index in reversed(range(BLOCK_SIZE)):

        for byte_value in range(MAX_BYTE_VALUE+1):
            modified_iv[iv_index] = byte_value
            # modified_ct = hexlify(modified_iv + cookies)
            # io.sendlineafter(b"? ", modified_ct)
            # response = io.recvline().decode().strip().encode()
            keystream[ks_index] = byte_value ^ padding
            # print(keystream[ks_index] ^ original_iv[iv_index], int(pt[iv_index]))
            # print(keystream[ks_index] ^ original_iv[iv_index]), pt[iv_index])
            if keystream[ks_index] ^ original_iv[iv_index] == pt[iv_index]:
                # print(chr(keystream[ks_index] ^ original_iv[iv_index]), pt[iv_index])
                # print(f"Valid iv byte: {hex(byte_value)}")
                keystream[ks_index] = byte_value ^ padding
                # print(f"Keystream bytes: {[hex(byte) for byte in keystream]}")

                plaintext.append(keystream[ks_index] ^ original_iv[iv_index])
                # print(f"Plaintext bytes: {[hex(byte) for byte in plaintext]}")

                break

        padding += 1
        modified_iv = compute_next_valid_iv_byte(keystream, padding, modified_iv)
        ks_index += 1
    plaintext_chars = ''.join(chr(byte) for byte in reversed(plaintext))
    print(f"Complete Decrypted Text: {plaintext_chars}")
    return keystream

def dump_user(user):
    def try_to_bytes(x):
        if type(x) == bytes:
            return x
        elif type(x) == str:
            return x.encode()
        else:
            return str(x).encode()
    return b"&".join(key.encode()+b"="+try_to_bytes(value) for key, value in user.items())

io = remote(HOST, PORT, ssl=True)

username = b"AAAAAAA"
payload = pad(b"True", AES.block_size)
payload = username + payload + b"AAAAaaaaa"
user = {"username": payload, "admin": b"False"}
cookie_pt = dump_user(user)
blocks = [cookie_pt[i: i+16] for i in range(0,len(cookie_pt), +16)]
blocks[-1] = pad(blocks[-1], AES.block_size)

io.sendlineafter(b"? ", payload)
ct = io.recvline().decode().split()[-1]
ct = bytes.fromhex(ct)
blocks_ct = [ct[i: i+16] for i in range(0,len(ct), +16)]
print(blocks)

keystream1 = oracle_padding(bytearray(blocks_ct[-5]), bytearray(blocks_ct[-4]), bytearray(blocks[-4]))
keystream2 = oracle_padding(bytearray(blocks_ct[-4]), bytearray(blocks_ct[-3]), bytearray(blocks[-3]))
keystream3 = oracle_padding(bytearray(blocks_ct[-3]), bytearray(blocks_ct[-2]), bytearray(blocks[-2]))
keystream4 = oracle_padding(bytearray(blocks_ct[-2]), bytearray(blocks_ct[-1]), bytearray(blocks[-1]))

# print(keystream1)
# print(len(blocks_ct[-5]))
# for i, k in zip(keystream1, blocks_ct[-5]):
#     # print(i, k)
#     print(hex(i ^ k), end="-")

# print("\n", blocks_ct[-4])

t = pad(b"True", AES.block_size)
f = pad(b"False", AES.block_size)

delta = b""
for i, k in zip (t,f):
    delta += bytes(i^k)

for i, k in zip(delta, blocks[-4]):
    blocks[-4] = bytes(i^k)

io.sendlineafter(b"? ", b"".join(blocks_ct))
print(io.recvline())
io.close()
# user = {"username": username.encode() + payload + b"AAAAaaaaa", "admin": b"False"}
# cookie_pt = dump_user(user)

# blocks = [cookie_pt[i: i+16] for i in range(0,len(cookie_pt), +16)]
# for i in blocks:
#     print(i)

# print(cookie_pt)
# print(cookie_pt[len(cookie_pt)-16:])
# print(len(cookie_pt[-16:]))


# io = remote(HOST, PORT, ssl=True)
# io.recvline()
# encrypted_data = io.recvline().decode().strip().encode()
# oracle_padding(ciphertext=encrypted_data)