from Crypto.Util.number import bytes_to_long, long_to_bytes

def steplfsr(lfsr):
    b7 = (lfsr >> 7) & 1
    b5 = (lfsr >> 5) & 1
    b4 = (lfsr >> 4) & 1
    b3 = (lfsr >> 3) & 1

    feedback = b7 ^ b5 ^ b4 ^ b3
    lfsr = (feedback << 7) | (lfsr >> 1)
    return lfsr

def verita():
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    print(a,b,c,d,"    ",a^b^c^d)

ct = "21c1b705764e4bfdafd01e0bfdbc38d5eadf92991cdd347064e37444e517d661cea9"
ct = bytes.fromhex(ct)

# verita()

# count = 0
# leng = []

for i in range(256):
    output = bytearray()
    lfsr = i
    for p in ct:
        lfsr = steplfsr(lfsr)
        ks = lfsr
        output.append(p ^ ks)
    try:
        pt = bytes(output).decode()
        if "picoCTF" in pt:
            print(pt)
            exit()
    except BaseException:
        pass

# print(len(bin(int("ff", 16))[2:]))