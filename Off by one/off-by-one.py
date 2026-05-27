#!/usr/bin/env python3

import secrets
import os

flag = os.getenv("FLAG", "CCIT{example_flag}")

p = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E08"
    "8A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B"
    "302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9"
    "A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE6"
    "49286651ECE65381FFFFFFFFFFFFFFFF",
    16,
)
g = 2

_LCG_A = 1337
_LCG_C = 23648563168735083182988073175367160757783412266605083936805699537689016851317252976634838192074944198851091943900758944045300883215384121118734114275597966898448616815143213102146763076078302464707523959600214810708910571027151288789578730770032334264878553014887312329744960260462899281578393297060117831153
_lcg_state = secrets.randbelow(p)


def _next_k(p: int) -> int:
    global _lcg_state
    _lcg_state = (_LCG_A * _lcg_state + _LCG_C) % p
    return _lcg_state


def generate_keys(p: int, g: int):
    x = secrets.randbelow(p)
    y = pow(g, x, p)
    return (p, g, y), x


def encrypt(message: int, public_key):
    p, g, y = public_key

    if not (1 <= message < p):
        raise ValueError("message must satisfy 1 <= message < p")

    k = _next_k(p)
    c1 = pow(g, k, p)
    s = pow(y, k, p)
    c2 = (message * s) % p
    return c1, c2


def decrypt(ciphertext, private_key, p):
    c1, c2 = ciphertext
    s = pow(c1, private_key, p)
    s_inv = pow(s, p - 2, p)
    return (c2 * s_inv) % p


msgs = [secrets.randbelow(p) for _ in range(2)]
public_key, private_key = generate_keys(p, g)
print(public_key)
ciphertexts = [encrypt(msg, public_key) for msg in msgs]
print("Hints: ", ciphertexts)

your_msg = input("> ").split(',')

your_msg = [int(x) for x in your_msg]
print(decrypt(your_msg, private_key, p))

guess0 = input("> ")
guess1 = input("> ")

if int(guess0) == msgs[0] and int(guess1) == msgs[1]:
    print(flag)
else:
    print("Wrong guess")

