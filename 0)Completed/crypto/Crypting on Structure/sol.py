def binario(ct):
    b = ""
    for i in ct:
        if i == 'A':
            b += '0'
        else:
            b += '1'
    return b

def blocchi(ct):
    blocks = []
    for i in range(0, len(ct), 5):
        blocks.append(ct[i:i + 5])
    return blocks

ct = "AAAABAAAAAAAABAABBBAABBABABAAABAABABAABAABBBABAABBAAAAABAABABAABBBBAAA"
ct = blocchi(ct)
# print(ct)

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O','P','Q','R','S','T','U','V','W','X','Y','Z']

pt = "flag{"
for b in ct:
    b = binario(b)
    b = int(b, 2)
    # print(b)
    pt += alpha[b]
pt += "}"

print(pt)


