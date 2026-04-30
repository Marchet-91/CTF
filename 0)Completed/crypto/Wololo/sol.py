sub = {"B": "I", "T": "A", "c": "g", "u": "e", "x": "o", "i":"f",
       "U": "E", "n": "m", "j": "p", "b": "i", "p": "r", "N":"M",
       "e": "c", "v": "t", "t": "a", "f": "n", "k": "h", "q":"d",
       "l": "u", "a": "v", "w": "l", "V": "T", "O": "R", "h":"b",
       "d": "y", "P": "R", "g": "z", "J": "P", "z": "w", "Z":"W"}

with open("ciphertext.txt", "r") as f:
    ct = f.readline()

print(ct, end="\n\n")

sol = ""
for i in ct:
    if sub.get(i, 0) != 0:
        sol += sub[i]
    else: 
        sol += i

print(sol)

# srdnlen{AGE_OF_EMPIRES_II}