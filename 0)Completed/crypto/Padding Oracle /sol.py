#!/usr/bin/env python3
from binascii import hexlify, unhexlify
from time import sleep
import logging
from pwn import *

# Constants
BLOCK_SIZE = 16
MAX_BYTE_VALUE = 255
HOST = "padding-oracle.chall.srdnlen.it"
PORT = 443

def compute_next_valid_iv_byte(keystream, padding, modified_iv):
    for i in range(len(keystream)):
        next_iv = keystream[i] ^ padding
        modified_iv[len(modified_iv)-1-i] = next_iv
    return modified_iv


def oracle_padding(ciphertext):
    keystream = []
    plaintext = []

    original_ct = bytearray(unhexlify(ciphertext))
    original_iv = original_ct[-96:-80]
    cookies = original_ct[-80:-64]
    print(original_iv)
    print(cookies)

    modified_iv = bytearray(b'0000000000000000')
    padding = 0x01
    ks_index = 0
    for iv_index in reversed(range(BLOCK_SIZE)):

        for byte_value in range(MAX_BYTE_VALUE+1):
            modified_iv[iv_index] = byte_value
            modified_ct = hexlify(modified_iv + cookies)
            io.sendlineafter(b"? ", modified_ct)
            response = io.recvline().decode().strip().encode()

            if b"Wow you are so strong at decrypting!" in response:

                print(f"Valid iv byte: {hex(byte_value)}")
                keystream.append(byte_value ^ padding)
                print(f"Keystream bytes: {[hex(byte) for byte in keystream]}")

                plaintext.append(keystream[ks_index] ^ original_iv[iv_index])
                print(f"Plaintext bytes: {[hex(byte) for byte in plaintext]}")

                break

        padding += 1
        modified_iv = compute_next_valid_iv_byte(keystream, padding, modified_iv)
        ks_index += 1
    plaintext_chars = ''.join(chr(byte) for byte in reversed(plaintext))
    print(f"Complete Decrypted Text: {plaintext_chars}")


io = remote(HOST, PORT, ssl=True)
io.recvline()
encrypted_data = io.recvline().decode().strip().encode()
oracle_padding(ciphertext=encrypted_data)

# srdnlen{and_then_zeus_turned_himself_into_a_pickle_80e6d84ba22c}