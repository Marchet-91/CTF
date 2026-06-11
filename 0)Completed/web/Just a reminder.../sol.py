from requests import * 
from base64 import b64decode
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

data = b64decode("U2FsdGVkX1/JEKDXgPl2RqtEgj0LMdp8/Q1FQelH7whIP49sq+WvNOeNjjXwmdrl")

salt = data[8:16]
ct = data[16:]

def evp_bytes_to_key(password, salt, key_len, iv_len):
    d = b""
    last = b""
    while len(d) < key_len + iv_len:
        last = md5(last + password + salt).digest()
        d += last
    return d[:key_len], d[key_len:key_len+iv_len]

key, iv = evp_bytes_to_key(b"ML4czctKUzigEeuR", salt, 32, 16)

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct), 16)

passw = pt.decode()

URL = "http://just-a-reminder.challs.olicyber.it"
JS = "/default.js"

# flag{d0n7_u53_cl13n7_51d3_ch3ck5!!}