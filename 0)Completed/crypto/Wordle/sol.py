ct = open("output.txt", "r").readline()

diz = {
    'c': 'f', 'y':'l', 'v': 'a',
    'z': 'g'

}

pt = ""
for c in ct: 
    if diz.get(c, 0) == 0:
        pt += c
    else:
        pt += diz[c]

print(ct)
print(pt)

# SIto utile: https://quipqiup.com/
# nobody cares if this is the wrong website as long as it contains the flag: flag{cryptoquips_are_born_to_be_broken}