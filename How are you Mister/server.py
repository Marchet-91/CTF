from Crypto.Hash import MD5 
import codecs 
import random 
import os 
 
FLAG = os.environ['FLAG'] 
 
key = str(random.getrandbits(64)) 
 
 
def sign(message): 
    h = MD5.new() 
    h.update(key.encode()) 
    h.update(message)
    print(h.hexdigest()) 
 
 
def verify(message, message_digest): 
    h = MD5.new() 
    h.update(key.encode()) 
    h.update(message) 
    if h.hexdigest() == message_digest:
        return True 
    else: 
        return False 
 
 
menu = ("""Hello, what do you want to do?\n""" 
        """1. Sign a message\n""" 
        """2. Verify a message\n""" 
        """3. Quit\n> """) 
 
 
def start_server(): 
    while True: 
 
        choice = input(menu) 
 
        if choice == '1': 
            try: 
                message = input("Insert your name (hex format)? ") 
                message = bytearray.fromhex(message) 
 
                if 'admin' in codecs.decode(message, 'utf-8', 'ignore'): 
                    print("No fake admin") 
                    continue 
                sign(message) 
            except: 
                print("Only hex data") 
 
        if choice == '2': 
 
            message = input("Insert your name (hex format)? ") 
            message_digest = input("Insert relative signature ") 
            message = bytearray.fromhex(message) 
            if verify(message, message_digest): 
                if 'admin' in codecs.decode(message, 'utf-8', 'ignore'): 
                    print("Welcome mr admin this is your flag", FLAG) 
                    break 
                else: 
                    print("Welcome how are you?") 
            else: 
                print("Incorrect") 
 
        if choice == '3': 
            print("Bye Bye") 
            exit() 
 
 
if __name__ == "__main__": 
    print(len(key)) 
    start_server()