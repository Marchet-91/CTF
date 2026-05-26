#!/usr/bin/env python3

import os

flag = os.getenv('FLAG', 'CCIT{redacted}')
flag = bin(int.from_bytes(flag.encode(), "big"))

while True:
    your_flag = input("flag: ")
    if your_flag == "":
        break
    rev_score = 0
    for i in range(len(your_flag)):
        if your_flag[i] == flag[i]:
            rev_score += 1
    print(f"{rev_score = }")
