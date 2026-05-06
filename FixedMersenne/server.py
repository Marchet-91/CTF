import os
import random

FLAG = os.environ['FLAG']
TRIES = 1337 % 1000

print("|  I found a way to patch the Mersenne Twister PRNG.")
print("|  All you have to do is generate numbers with one bit less than a multiple of 32")
print("|  and you've defeated all attackers!\n|")

print("|  If you don't believe me, try to break this by guessing the number I will generate after these ones:")
for _ in range(4):
    print(f"|  {random.getrandbits(624 * 8 - 1)}")
x = random.getrandbits(624 * 8 - 1)
print("|  I will even give you almost as many tries as you want :)")

for _ in range(TRIES):
    x_guess = int(input("|  >>> "))
    if x == x_guess:
        break
    else:
        print("|  Nope... just as I told you... zzzz")
else:
    exit("|  See, you can't break it and you will never do... now I need to go, byeeee!")

print("|  What? Well... you saved me, I was about to publish a paper on this.")
print(f"|  You didn't see anything, and this flag will keep your mouth shut: {FLAG}")
