ct = "xqkwKBN{z0bib1wv_l3kzgxb3l_25l7k61j}"

for i in range(26):
    pt = ""
    for j in range(len(ct)):
        if ct[j].islower():
            pt += chr((ord(ct[j]) - ord('a') + i) % 26 + ord('a'))
        elif ct[j].isupper():
            pt += chr((ord(ct[j]) - ord('A') + i) % 26 + ord('A'))
        else:
            pt += ct[j]
    if "pico" in pt:
        print(pt)
        exit()