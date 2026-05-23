from z3 import *

# Solver
s = Solver()

# Variabili simboliche
x = Int("x")
y = Int("y")

# Constraints
s.add(x > 0)
s.add(y > 0)
s.add(x + y == 10)
s.add(x > y)

# Check
if s.check() == sat:
    m = s.model()
    print("[+] SAT")
    print("x =", m[x])
    print("y =", m[y])
else:
    print("[-] UNSAT")