from pwn import * 
from Crypto.Util.number import long_to_bytes

HOST = "rev-chall.challs.cyberchallenge.it"
PORT = 38211

# context.log_level = 'debug'
# io = process(["python3","rev_chall.py"])
io = remote(HOST, PORT)

flag = "0b"
pos = ['1','0', '2']
point = 0

b = "0b1000011010000110100100101010100011110110011010001101110011001000101111101110100011010000011001101011111011000100011001101110011011101000101111101110010001100110111011001011111011100000110110000110100011110010011001101110010010111110011010001110111001101000111001001100100010111110110011100110000001100110111001101011111011101000011000001011111011001000011010100110011001101010110000100110010001101110011010001111101"
flag = int(b, 2).to_bytes((int(b, 2).bit_length() + 7) // 8, "big").decode()
print(flag)

while True:
    last = point
    for c in pos:
        tmp = flag + c
        # print(tmp)
        io.sendlineafter(b": ", tmp.encode())
        try:
            ris = io.recvline().strip()
        except EOFError:
            io.close()
            io = remote(HOST, PORT)
            io.sendlineafter(b": ", tmp.encode())
            ris = io.recvline().strip()
        # print(ris.decode().split("=")[-1])
        ris = int(ris.decode().split("=")[-1])
        if ris > point:
            point = ris
            flag = tmp
            print(flag)
            break
    if last == point:
        flag = int(flag, 2).to_bytes((int(flag, 2).bit_length() + 7) // 8, "big").decode()
        print(flag)
        exit()
