from string import printable
from Crypto.Cipher import AES
import binascii, sys

KEY = "yn9RB3Lr43xJK2".encode()
msg = "AES with CBC is very unbreakable".encode()
pt1 = "AES with CBC is ".encode()
pt2 = "very unbreakable".encode()
A = "c5██████████████████████████d49e"
B = "78c670cb67a9e5773d696dc96b78c4e0"
ivMid = bytes.fromhex("c5") + b"a"*13 + bytes.fromhex("d49e") # 16
# print(len(ivMid))

# b'yn9RB3Lr43xJK2T$' b'0AAAAAAAAAAAAA4H'

def key():
    for a in printable:
        for b in printable:
            key = KEY
            tmp = key + a.encode() + b.encode()
            # print(key)
            cipher = AES.new(tmp, AES.MODE_CBC, ivMid)
            pt = cipher.decrypt(bytes.fromhex(B))
            if pt[0] == ord('v') and pt[-2] == ord('l') and pt[-1] == ord('e'):
                return tmp
            
def find_ct1(key):
    ct1 = ""
    for c in range(13):
        # print(c+1)
        for i in range(256):
            ivMid = bytes.fromhex("c5") + bytes.fromhex(ct1) + i.to_bytes() + b"a"*(13 - len(bytes.fromhex(ct1)) - 1) + bytes.fromhex("d49e")
            # print(c)
            aes = AES.new(key, AES.MODE_CBC, ivMid)
            pt = aes.decrypt(bytes.fromhex(B))
            if pt[c + 1] == pt2[c+1]:
                # print(pt[c+1])
                # input()
                ct1 += binascii.hexlify(i.to_bytes()).decode()
                break
    return "c5" + ct1 + "d49e"

def find_iv(key, ct1):
    iv = b""
    for c in range(16):
        # print(c+1)
        for i in range(256):
            ivMid = iv + i.to_bytes() + b"a"*(16 - len(iv) - 1)
            # print(ivMid)
            aes = AES.new(key, AES.MODE_CBC, ivMid)
            pt = aes.decrypt(bytes.fromhex(ct1))
            if pt[c] == pt1[c]:
                # print(pt[c+1])
                # input()
                iv += i.to_bytes() 
                break
    return iv

fullKey = key()
# print(fullKey)
ct1 = find_ct1(fullKey)
# print(ct1)
iv = find_iv(fullKey, ct1)
print("CCIT{" + iv.decode() + "}")
