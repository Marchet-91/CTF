def decode(i, ct):
    pt = ""
    for j in range(len(ct)):
        if ct[j] >= 'A' and ct[j] <= 'Z':
            pt += chr((ord(ct[j]) - ord('A') - i) % 26 + ord('A'))
            # print(pt)
        elif ct[j] >= 'a' and ct[j] <= 'z':
            pt += chr((ord(ct[j]) - ord('a') - i) % 26 + ord('a'))
        else:
            pt += ct[j]
    return pt

ct = "CVOXNOB XED CMYBZSYX GOSBN"

for i in range(27):
    print(i,    decode(i, ct))