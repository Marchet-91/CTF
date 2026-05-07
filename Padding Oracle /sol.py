from pwn import *

def recover_block(ct, i, io):
    # ct[i-1] = blocco che modifichi
    # ct[i]   = blocco target

    prev = ct[i-1]
    curr = ct[i]

    intermediate = bytearray(16)
    modified = bytearray(prev)
    for pos in range(15, -1, -1):
        padding = 16 - pos  # 0x01, 0x02, ...
        # aggiorna i byte già risolti per mantenere padding corretto
        for j in range(pos+1, 16):
            modified[j] = intermediate[j] ^ padding
        # brute force sul byte corrente
        for guess in range(256):
            modified[pos] = guess
            blocks = ct[:]
            blocks[i-1] = modified
            payload = b"".join(blocks)
            io.sendlineafter(
                b"What do you want to decrypt (in hex)? ",
                payload.hex().encode()
            )
            resp = io.recvline()
            if b"Wow you are so strong at decrypting!" in resp:   # dipende dal server
                intermediate[pos] = guess ^ padding
                print(intermediate)
                break

    return intermediate



HOST = "padding-oracle.chall.srdnlen.it"
PORT = 443

io = remote(HOST, PORT, ssl=True)

io.recvline()
ct = io.recvline().decode().strip()
ct = bytes.fromhex(ct)
ct = [bytearray(ct[i:i+16]) for i in range(0, len(ct), 16)]

print(len(ct))

keystream = []

for i in range(len(ct) - 1):
    keystream = keystream + [recover_block(ct, i, io)]

plaintext = []

for i in range(len(ct)-1):
    I = keystream[i]
    C_prev = ct[i - 1]
    
    plaintext_block = bytes([
        I[j] ^ C_prev[j]
        for j in range(16)
    ])
    
    plaintext.append(plaintext_block)

plaintext = b"".join(plaintext)
print(plaintext.decode())

io.close()