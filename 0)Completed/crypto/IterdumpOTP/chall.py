from Crypto.Random import random
from utils import randbits, strxor 

STRING_SIZE = 16
WINS_NEEDED = 750
TRIES = 1000


def encrypt(pt):
    bp = random.randint(0,1)
    if bp == 0:
        k = randbits(STRING_SIZE)
    else:
        k = randbits(1) * STRING_SIZE
       
    ct = strxor(k, pt)
    return ct
