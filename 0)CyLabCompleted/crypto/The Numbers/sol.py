ct = [16 ,9,3, 15, 3, 20, 6 , '{', 20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 13, 1, 19, 15, 14, "}"]

for c in ct:
    if type(c) == int:
        print(chr(c + ord('a') - 1), end="")
    else: 
        print(c, end="")

print()