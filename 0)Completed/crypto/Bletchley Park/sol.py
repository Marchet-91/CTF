key = [8,10,9,7,11,3,13,14,5,1,4,12,6,2]
#         x x         x x
# srdnlen{8_10_9_7_11_3_13_14_5_1_4_12_6_2}

with open("ciphertext.txt", "r") as f:
    ct = f.readline()

sol = ""
for i in range(0,len(ct),14):
    sol += ct[i + key[0] - 1]
    sol += ct[i + key[1] - 1]
    sol += ct[i + key[2] - 1]
    sol += ct[i + key[3] - 1]
    sol += ct[i + key[4] - 1]
    sol += ct[i + key[5] - 1]
    sol += ct[i + key[6] - 1]
    sol += ct[i + key[7] - 1]
    sol += ct[i + key[8] - 1]
    sol += ct[i + key[9] - 1]
    sol += ct[i + key[10] - 1]
    sol += ct[i + key[11] - 1]
    sol += ct[i + key[12] - 1]
    sol += ct[i + key[13] - 1]

# print(sol)

first = list(ct[:14])
firstE = True
encrypt = "srdnlen{"
for c in "Bletchley Park":
    for pos, ct in enumerate(first):
        if c == ct:
            if firstE and c == "e":
                firstE = False
                continue
            encrypt += str(pos + 1) + "_"
            first[pos]= "X"

print(encrypt[:-1] +"}")
#Bletchley Park
# khPyrtBelcale
#
#srdnlen{7_9_8_6_10_3_13_14_1_4_12_6_2}
#srdnlen{7_9_14_6_10_3_9_8_1_4_12_6_2}
#srdnlen{7_13_8_6_10_3_9_14_1_4_12_6_2}
#srdnlen{7_13_14_6_10_3_9_8_1_4_12_6_2}
#          x x        x   x