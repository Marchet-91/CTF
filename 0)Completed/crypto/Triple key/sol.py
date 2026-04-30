from Crypto.Util.number import long_to_bytes, bytes_to_long

def mixkeybit(keybit1, keybit2, keybit3):
    return int(keybit1 or (not(keybit2) and keybit3))

with open("output.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

flagB = ""
for i in range(len(lines[0])):
    ones = sum(int(line[i]) for line in lines)
    
    if ones > len(lines) // 2:
        flagB += "0"
    else:
        flagB += "1"

print(long_to_bytes(int(flagB,2)).decode())