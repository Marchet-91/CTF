from sympy.ntheory.modular import crt

mod = [5,11, 17]
res = [2,3,5]

x, m = crt(mod, res)

print(x % 935)

