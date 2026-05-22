#!/usr/bin/env python3

import signal
import os
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

TIMEOUT = 120
BANNER = """
   ___   ________  __            __    __  ___        __      ____  ___  ____                    __  _         
  / _ | / __/ __/ / /  ___  ___ / /_  /  |/  /__  ___/ /__   / __ \/ _/ / __ \___  ___ _______ _/ /_(_)__  ___ 
 / __ |/ _/_\ \  / /__/ _ \(_-</ __/ / /|_/ / _ \/ _  / -_) / /_/ / _/ / /_/ / _ \/ -_) __/ _ `/ __/ / _ \/ _ \\
/_/ |_/___/___/ /____/\___/___/\__/ /_/  /_/\___/\_,_/\__/  \____/_/   \____/ .__/\__/_/  \_,_/\__/_/\___/_//_/
                                                                           /_/                                 
"""
MENU = """
What do you want to do?
1) Generate your cookie
2) Cookie login
*) Exit
"""

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert(flag.startswith("srdnlen{"))
assert(flag.endswith("}"))

key = os.urandom(32)


class AES_PCBC():
    def __init__(self, key: bytes):
        """Implementation of AES PCBC mode of operation"""
        self.key = key
    
    def encrypt(self, pt: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = pad(pt, AES.block_size)
        iv = os.urandom(AES.block_size)
        xor_block = iv

        ct = []
        for i in range(len(pt) // AES.block_size):

            ct.append(cipher.encrypt(strxor(pt[i * 16:(i + 1) * 16], xor_block)))
            xor_block = strxor(pt[i * 16:(i + 1) * 16], ct[i])

        ct = b"".join(ct)

        return (iv + ct).hex()
    
    def decrypt(self, iv: bytes, ct: bytes) -> bytes:
        assert len(iv) == AES.block_size, f"iv length must be {AES.block_size}"
        assert len(ct) % AES.block_size == 0, f"ct length must be multiple of {AES.block_size}"
        cipher = AES.new(self.key, AES.MODE_ECB)
        xor_block = iv

        pt = []
        for i in range(len(ct) // AES.block_size):
            
            pt.append(strxor(cipher.decrypt(ct[i * 16:(i + 1) * 16]), xor_block))
            xor_block = strxor(ct[i * 16:(i + 1) * 16], pt[i])

        pt = unpad(b"".join(pt), AES.block_size)

        return pt.hex()


def main():
    print(BANNER)
    while True:
        try:
            print(MENU)
            choice = int(input(">>> "))

            if choice == 1:
                username = bytes.fromhex(input("Insert your username: (hex) "))
                if b"admin" in username:
                    print("Only real admins can sign themselves as admins")
                    continue
                cookie = AES_PCBC(key).encrypt(username)
                print(f"Here's your hex encoded cookie: {cookie}")

            elif choice == 2:
                cookie = bytes.fromhex(input("Insert your cookie: (hex) "))
                username = bytes.fromhex(AES_PCBC(key).decrypt(cookie[:AES.block_size], cookie[AES.block_size:]))
                if b"admin" in username:
                    print(f"Welcome back admin#{username.hex()}, we have a something for you...")
                    print(f"Here's your flag, just keep it secret: {flag}")
                else:
                    print(f"Welcome back user#{username.hex()}, today we have nothing for you, but tomorrow... who knows")

            else:
                print("Byeee")
                break

        except ValueError as e:
            print(e)
        except AssertionError as e:
            print(e)


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    main()
