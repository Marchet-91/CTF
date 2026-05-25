#!/bin/python3

import os
import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64decode

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert(flag.startswith("CCIT{"))
assert(flag.endswith("}"))

TIMEOUT = 300
k1, k2 = None, None
users = []
nonce = None
admin = b'default_server_admin'

def compress(l):
    l = [l[i:i+16] for i in range(0,len(l),16)]
    l = [int.from_bytes(l_, 'big') for l_ in l]
    return (sum(l) & (2**128 - 1)).to_bytes(16, 'big')

def init_server():
    global k1, k2, nonce, users
    k1, k2 = os.urandom(32), os.urandom(32)
    nonce = os.urandom(8)
    users.append(admin)
    return

def sign(data):
    cipher = AES.new(k1, AES.MODE_CTR, nonce=nonce)
    enc_data = cipher.encrypt(pad(data, 16))
    compressed = compress(enc_data)

    cipher = AES.new(k2, AES.MODE_ECB)
    tag = cipher.encrypt(compressed).hex()
    return tag

def verify(data, tag):
    return sign(data) == tag

def register():
    global users
    username = b64decode(input('Username (base64 encoded): ').encode())
    if username in users:
        print('Name already taken!')
        return
    token = sign(username)
    users.append(username)
    print(f'Registration successful. Here\'s your token: {token}')
    return

def login():
    global users
    username = b64decode(input('Username (base64 encoded): ').encode())
    token = input('Token: ')
    if username in users:
        if verify(username, token):
            print('Login successful!')
            return username
    print('Invalid credentials.')
    return None

def menu():
    print('''
1) register
2) login
3) quit''')
    return input('\n> ')

def handle():
    while 1:
        choice = menu()
        if choice == '1':
            register()
        elif choice == '2':
            username = login()
            if username == admin:
                print(flag)
                break
        else:
            break
    return

if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    init_server()
    handle()