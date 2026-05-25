from math import * 

p= 29
ask=[14,6,11]

for n in ask:
    for i in range(p):
        if int(pow(i, 2)) % p == n:
            print(n, i)