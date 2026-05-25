#!/bin/env python3

from Crypto.Util.number import getStrongPrime, bytes_to_long
from hashlib import sha1
import string
import random
import os
import signal

TIMEOUT = 300

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("CCIT{"))
assert(FLAG.endswith("}"))

alph = string.ascii_lowercase + string.ascii_uppercase + string.digits


def get_string(N):
    return ''.join(random.choice(alph) for _ in range(N))


p, q = getStrongPrime(512), getStrongPrime(512)
n = p*q
e = 65537
phi = (p-1)*(q-1)
d = pow(e, -1, phi)


def sign(m):
    m_hash = bytes_to_long(sha1(m).digest())
    exp = d*m_hash
    signed = pow(2, exp, n)
    return hex(signed)[2:].rjust(256, '0')


def verify(m, s):
    try:
        m_hash = bytes_to_long(sha1(m).digest())
        signed = pow(2, m_hash, n)
        check = pow(int(s.decode(), 16), e, n)
        return signed == check
    except:
        return False


def handle():

    print("||================================================================||")
    print("|| Welcome to the worst (not so) RSA-based signature service ever ||")
    print("||================================================================||")

    for _ in range(4):

        print()
        print("What do you want to do?")
        print()
        print("1. Sign a message")
        print("2. Verify a signature")
        print("3. Start the challenge")
        print("4. Print modulus")
        print("0. Exit")

        c = input("> ").encode().strip()

        if c == b"1":
            m = input("Give me the message: ").encode().strip()
            s = sign(m)
            print(f"The signature for the message is: {s}")
        elif c == b"2":
            m = input("Give me the message: ").encode().strip()
            s = input("Give me the signature: ").encode().strip()
            print(f"The result of the verification is: {verify(m, s)}")
        elif c == b"3":
            for __ in range(10):
                m = get_string(20)
                s = input(f"What is the signature of {m}? ").encode().strip()
                if s != sign(m.encode()).encode():
                    print("Sorry, that's wrong")
                    return
            print(FLAG)
        elif c == b"4":
            print(f"The modulus is: {n}")
        else:
            return


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
