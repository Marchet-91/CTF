ct = "xcqv{gvyavn_zvztv_etvtddlnxcgy}"

alphabet = "abcdefghijklmnopqrstuvwxyz"

def decrypt(cipher, key):
    plaintext = ""

    for character in cipher:
        if 'a' <= character <= 'z':
            # key = key[1:] + key[0]
            i = key.index(character)
            plain = alphabet[i]
            # undo della rotazione a destra
            key = "".join([key[len(key)-1:],key[0:len(key)-1]])
            # print(key)
            plaintext += plain
        else:
            plaintext += character

    return plaintext

for i in range(26):
    key = "".join([alphabet[i:], alphabet[0:i]])
    pt = decrypt(ct, key)
    if "flag" in pt:
        print(pt)
        exit()