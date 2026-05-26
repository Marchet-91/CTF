from pwn import *
import binascii

r = remote("recycle.challs.cyberchallenge.it", 38213)  # ip:port del servizio

# Step 1: Ottieni i keystream per molti counter iniziali
keystream = []
n_blocks = 100  # abbastanza per il flag
for i in range(n_blocks):
    r.sendlineafter(b"> ", b"1")
    data = r.recvline().decode().strip().split()
    plain_hex, cipher_hex = data[0], data[1]
    plain = bytes.fromhex(plain_hex)
    cipher = bytes.fromhex(cipher_hex)
    ks = bytes(a ^ b for a, b in zip(plain, cipher))
    keystream.append(ks)

# Step 2: Ottieni flag ciphertext
r.sendlineafter(b"> ", b"2")
flag_cipher_hex = r.recvline().decode().strip()
flag_cipher = bytes.fromhex(flag_cipher_hex)

# Step 3: Decrypt flag
flag_blocks = [flag_cipher[i*16:(i+1)*16] for i in range(len(flag_cipher)//16)]
flag = b""
for i, block in enumerate(flag_blocks):
    flag += bytes(a ^ b for a, b in zip(block, keystream[i]))

print(flag.decode())