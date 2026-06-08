import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
from signal import alarm as timeout
FLAG = b"????"


def key_exchange():
    g, p = open('./data').read().split()
    g, p = int(g, 16), int(p, 16)
    Alice_private = int.from_bytes(os.urandom(156), 'big') % p
    Alice_public = pow(g, Alice_private, p)
    print(json.dumps({"g": g, "p": p, "A": Alice_public}))

    Bob_private = int.from_bytes(os.urandom(156), 'big') % p
    Bob_public = pow(g, Bob_private, p)
    print(json.dumps({"B": Bob_public}))

    Alice_Shared_secret = pow(Bob_public, Alice_private, p)
    Bob_Shared_secret = pow(Alice_public, Bob_private, p)
    Shared_secret = pow(g, Alice_private * Bob_private, p)
    assert(Alice_Shared_secret == Bob_Shared_secret)
    assert(Alice_Shared_secret == Shared_secret)

    key = (Shared_secret % (2**(8*16) - 1)).to_bytes(16, 'big')
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    print("flag: " + b64encode(ciphertext).decode())


def corrupt_data():
    with open('./data', 'w') as file:
        data = input("Abbiamo accesso al file usato per decidere i parametri crittografici su questa rete XD Puoi mettere quello che vuoi, quindi divertiti e spiali per bene!\n Sovrascrivi file con: ")
        file.write(data)


def main():
    corrupt_data()
    key_exchange()


if __name__ == '__main__':
    timeout(300)
    main()
