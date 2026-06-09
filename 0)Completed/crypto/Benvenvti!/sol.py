ct = "synt{Orairahgv_nyyn_pgs!}"

i = 13
flag = ""
for j in range(len(ct)):
    if ct[j].isalpha():
        if ord(ct[j]) > ord('a'):
            flag += chr((ord(ct[j]) - ord('a') + i) % 26 + ord('a'))
        else:
            flag += chr((ord(ct[j]) - ord('A') + i) % 26 + ord('A'))
    else:
        flag += ct[j]

print(flag)