import os
from Crypto.Cipher import AES

FLAG = os.getenv("FLAG", "srdnlen{redacted}")

SECRET_STRING = b"VerySecretString"

SECRET = os.urandom(16)
KEY = os.urandom(16)
IV = os.urandom(12)

for _ in range(4):
    try:
        choice = int(input("""What do you want to do?
                            1) Encrypt some text
                            2) Guess my secret""").strip())
        if choice == 1:
            plaintext = bytes.fromhex(input("Plaintext (hex): "))
            if SECRET_STRING not in plaintext:
                print("HARAM")
                continue
            plaintext = plaintext.replace(SECRET_STRING, SECRET, 1)
            cipher = AES.new(KEY, AES.MODE_GCM, nonce=IV)
            ciphertext, mac = cipher.encrypt_and_digest(plaintext)
            choice = int(input("""What do you want to know?
                                    1) Ciphertext
                                2) MAC""").strip())
            
            if choice == 1:
                print("Ciphertext:", b"lmfao you really thought I would give it to you!".hex())
            elif choice == 2:
                print("You can have it, it's just a hash after all:", mac.hex())
            else:
                print("Then you get nothing")
        elif choice == 2:
            guess = bytes.fromhex(input("Guess my secret (hex): "))
            if guess == SECRET:
                print(FLAG)
            else:
                print("Nuh uh")
            break
    except:
        print("Bad input")
        break
