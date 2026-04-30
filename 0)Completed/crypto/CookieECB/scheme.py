import codecs
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


key = None


def encrypt(pt):
    global key

    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)

    padded_pt = pad(pt, AES.block_size)
    byte_ct = cipher.encrypt(padded_pt)
    hex_ct = codecs.encode(byte_ct, 'hex')

    return hex_ct


def decrypt(ct):
    global key

    cipher = AES.new(key, AES.MODE_ECB)

    byte_ct = codecs.decode(ct, 'hex')
    padded_pt = cipher.decrypt(byte_ct)
    pt = unpad(padded_pt, AES.block_size)

    return pt
