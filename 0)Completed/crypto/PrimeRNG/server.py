import os
import random
from Crypto.Util.number import getPrime

FLAG = os.environ['FLAG']

ROUNDS = 32
TRIES = 32
SCHNEIER_FACTS = [
    "Bruce Schneier can write a recursive program that proves the Riemann Hypothesis. In Malbolge.",
    "The halting problem doesn't apply to Bruce Schneier. Loops terminate when he tells them to.",
    "Bruce Schneier knows Chuck Norris' private key.",
    "Bruce Schneier reads the 'Voynich Manuscript' as a bedtime story.",
    "Bruce Schneier never gets a speeding ticket because the camera manufacturers don't want to have to show him their source code in court.",
    "Hashes collide because they're swerving to avoid Bruce Schneier.",
    "Bruce Schneier has a set of SSH Bump Keys.",
    "Bruce Schneier can read captchas.",
    "Bruce Schneier is the root of all certificates.",
    "To describe the difficulty of cracking Bruce Schneier's cryptosystem, mathematicians use the term 'NP-Awesome'.",
]

print("|  Welcome to my new PRNG based on prime numbers")
print("|  Let's see if you're clever enough to break it :)\n|")

for _ in range(ROUNDS):
    p, q = getPrime(500), getPrime(500)
    x = getPrime(505)
    for _ in range(1337):
        x = (x * p - x * q) % 2 ** 1342
    
    print(f"|  Now guess my x (you have {TRIES} tries)")
    for _ in range(TRIES):
        x_guess = int(input("|  >>> "))
        if x_guess == x:
            print("|  You've earned it. Here's for you a Bruce Schneier random fact:")
            print(f"|  {random.choice(SCHNEIER_FACTS)}")
            break
        else:
            print("|  Nope :)")
    else:
        exit("|  Well clearly you need to look closely... maybe deeply into those numbers ;)")

print(f"|  Clearly you undestood the trick. Here's a flag for you {FLAG}.")
