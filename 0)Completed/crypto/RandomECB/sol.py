from pwn import * 
from string import printable

context.log_level = 'info'

logging.getLogger("pwnlib.tubes.remote").setLevel(logging.ERROR)

def search(pad, flag):

    for c in printable:
        # print(c)
        first = ""
        second = "B"
        while first != second:
            io = remote(HOST, PORT, ssl=True)

            io.sendlineafter(b"Input a string to encrypt (input 'q' to quit): ", CHECK * 2 + pad + flag + c.encode() + pad)
            io.recvline()
            response = bytes.fromhex(io.recvline().decode())
            first = response[:16]
            second = response[16:32]

            if first == second and response[64:64+16] == response[80+16+16:80+16+16+16]:
                return c

            io.close()

HOST = "randomecb.chall.srdnlen.it"
PORT = 443
flag = "srdnlen{n0w_0n3_r4nd0m_byt3_4t_4_t1m3}"
# print(len(flag))

for i in range(16):
    if flag[-1] == '}':
        break
    CHECK = ("B"*16).encode()
    pad = ("A" * (48 - 1 - len(flag))).encode()
    flag += search(pad, flag.encode())
    print(flag)

print()
