from chall import * 

def dump_user(user):
    def try_to_bytes(x):
        if type(x) == bytes:
            return x
        elif type(x) == str:
            return x.encode()
        else:
            return str(x).encode()
    return b"&".join(key.encode()+b"="+try_to_bytes(value) for key, value in user.items())


def load_user(user):
    try:
        fields = user.split(b'&')
        object = {}
        for field in fields:
            k, v = field.split(b'=')
            object[k.decode()] = v.strip()
        return object
    except:
        return None


username = b"AAAAAAAAAAAAAAAAAAAAAAAAAA" # To send
user = {"username": username, "admin": b"False"}
cookie_pt = dump_user(user)

for i in range(0, len(cookie_pt), 16):
    print(cookie_pt[i:i+16])

ct = encrypt(cookie_pt)
print(ct)
ct = codecs.decode(ct, "hex")
# print(ct)
cookie_pt = pad(cookie_pt, AES.block_size)

user = {"username": username, "admin": b"True"}
cookie_ch = pad(dump_user(user), AES.block_size)

new = b""

print(decrypt(codecs.encode(ct, "hex")))
print(len(ct))
print(len(cookie_ch))
print(cookie_pt)
print(cookie_ch)

ch = b"True\x02\x02"
new = ct[:-6]
j = 0
for i in range(len(ct) - 6, len(ct)):
    print(chr(cookie_pt[i - 16]), chr(ch[j]))
    keystream = ct[i - 16] ^ cookie_pt[i - 16]
    # print(keystream.to_bytes())
    new += (keystream ^ ch[j]).to_bytes()
    j += 1

# print(chr(cookie_pt[-6]))
# new += ct[-16]
# new += ct[-32:]
new = codecs.encode(new, "hex")
print(new)
print(decrypt(new))