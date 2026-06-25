from base64 import b64decode
from urllib.parse import unquote

ct = open("message.txt", "r").readline()

ct = unquote(bytes.fromhex(b64decode(ct).decode()))

key = 13
pt = ""

for c in list(ct): 
    if c.isalpha():
        if c.islower():
            pt += chr((ord(c) + key - ord('a')) % 26 + ord('a'))
        else: 
            pt += chr((ord(c) + key - ord('A')) % 26 + ord('A'))
    else:
        pt += c

print(pt)