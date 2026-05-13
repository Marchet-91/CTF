import codecs
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.strxor import strxor # MIo


key = None


def encrypt(pt):
    global key

    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_pt = pad(pt, AES.block_size)

    byte_ct = iv+cipher.encrypt(padded_pt)
    hex_ct = codecs.encode(byte_ct, 'hex')

    return hex_ct


def decrypt(ct):
    global key

    byte_fullct = codecs.decode(ct, 'hex')
    iv, byte_ct = byte_fullct[:16], byte_fullct[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    padded_pt = cipher.decrypt(byte_ct)
    try:
        print(padded_pt)
        pt = unpad(padded_pt, AES.block_size)
        return pt
    except:
        print("Bad padding!")
        return None
