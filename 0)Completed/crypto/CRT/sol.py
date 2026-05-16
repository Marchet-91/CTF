from z3 import *
from pwn import  * 

HOST = "crypto-10.challs.olicyber.it"
PORT = 30003

s = Solver()

x = Int('x')

s.add(x % 86 == 73)
s.add(x % 21 == 7)
s.add(x % 65 == 44)
s.add(x % 19 == 4)
s.add(x % 53 == 5)

if s.check():
    print(s.model())

# io.close()
