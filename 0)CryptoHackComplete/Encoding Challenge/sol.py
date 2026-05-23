from pwn import *
from Crypto.Util.number import long_to_bytes
import json
import base64
import codecs
import random

def decode(q):

    if q["type"] == "base64":
        sol = base64.b64decode(q["encoded"]).decode()
        # print(sol)
    elif q["type"] == "hex":
        sol = codecs.decode(q["encoded"], "hex").decode()
        # print(sol)
    elif q["type"] == "rot13":
        sol = codecs.decode(q["encoded"], "rot13")
        # print(sol)
    elif q["type"] == "bigint":
        sol = long_to_bytes(int(q["encoded"], 16)).decode()
        # print(sol)
    elif q["type"] == "utf-8":
        sol = "".join([chr(i) for i in q["encoded"]])
        # print(sol)

    return {"decoded": sol}


HOST = "socket.cryptohack.org"
PORT = 13377

io = remote(HOST, PORT)

for i in range(100):
    quest = json.loads(io.recvline())
    # print(i, quest)
    resp = json.dumps(decode(quest)).encode()
    io.sendline(resp)

print(io.recvline())

io.close()