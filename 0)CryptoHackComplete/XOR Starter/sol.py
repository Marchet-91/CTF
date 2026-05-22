from pwn import * 

ct = b"label"
val = 13

print(f"crypto{xor(ct, val).decode()}")