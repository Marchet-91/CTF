ct = "cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}"

for i in range(26):
    print(i, end=" ")
    for j in range(len(ct)): 
        if ct[j].islower():
            if ct[j] not in ["{", "}", "_"]:  
                print(chr((ord(ct[j]) + i - ord('a')) % 26 + ord('a')), end="")
            else:
                print(ct[j], end="")
        else:
            if ct[j] not in ["{", "}", "_"]:  
                print(chr((ord(ct[j]) + i - ord('A')) % 26 + ord('A')), end="")
            else:
                print(ct[j], end="")
    print()