from pwn import *

# K1=K3 (weak), K2 diverso
# 3DES con K1=K3 è involutorio!
WEAK_KEY = "0101010101010101" + "FEFEFEFEFEFEFEFE" + "0101010101010101"

io = remote("trouble.challs.cyberchallenge.it", 12000)

def encrypt(pt_hex, key_hex):
    io.recvuntil(b"> ")
    io.sendline(b"1")
    io.recvuntil(b"? ")
    io.sendline(pt_hex.encode())
    io.recvuntil(b"? ")
    io.sendline(key_hex.encode())
    return io.recvline().strip().decode()

def encrypt_flag(key_hex):
    io.recvuntil(b"> ")
    io.sendline(b"2")
    io.recvuntil(b"? ")
    io.sendline(key_hex.encode())
    return io.recvline().strip().decode()

c_flag = encrypt_flag(WEAK_KEY)
print(f"[*] Flag cifrato ({len(c_flag)//2} bytes): {c_flag}")

flag_bytes = b""
for i in range(0, len(c_flag), 16): 
    block = c_flag[i:i+16]
    if len(block) < 16:
        block = block.ljust(16, '0')
    result = encrypt(block, WEAK_KEY)
    flag_bytes += bytes.fromhex(result[:16])

print(flag_bytes)

io.close()