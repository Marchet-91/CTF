ct = "fzau{ncn_isors_cviovw_pwcqoze}"


def split(ct, size):
    size = len(ct) // size + (1 if len(ct) % size != 0 else 0)
    blocks = [""] * size

    for pos, i in enumerate(ct):
        blocks[pos % size] += i
    return blocks

ct = "".join([s if s.isalpha() else ""  for s in ct])

def index_of_coincidence(ct):
    freq = {}

    for i in ct:
        if freq.get(i, 0) == 0:
            freq[i] = 1
        else: 
            freq[i] += 1
    
    somma = 0
    for val in freq.values():
        somma += val *(val - 1)

    if somma == 0:
        return 0

    return somma / (len(ct) *(len(ct) - 1))


# print(len(ct))
max = -1
for i in range(2, len(ct)):
    blocks = split(ct, i)

    somma = 0
    for b in blocks: 
        somma += index_of_coincidence(b)
    
    if max < somma / len(blocks):
        max = somma  /len(blocks)
        key_size = i

# print(key_size)
key = [0,12]
# print(len(key))
# for i in range(256):
#     if ord(ct[1]) ^ i == ord("l"):
#         key[1] = i
#     if ord(ct[3]) ^ i == ord("g"):
#         key[3] = i
    
#     if key[1] != 0 and key[2] != 0:
#         break

ct = open("ct.txt", "r").readline()
pt = ""
i = 0
for c in ct: 
    if c.isalpha():
        pt += chr((ord(c) - ord('a') + key[i % 2]) % 26 + ord('a'))
        i += 1
    else: 
        pt += c

print(pt)