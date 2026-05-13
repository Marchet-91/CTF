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
print(cookie_pt)
print(cookie_ch)
for i in range(16, len(cookie_pt), 1):
    keystream = ct[i - 16] ^ cookie_pt[i]
    # print(keystream.to_bytes())
    new += (keystream ^ cookie_ch[i]).to_bytes()

new += ct[-32:]
new = codecs.encode(new, "hex")
print(new)
print(decrypt(new))