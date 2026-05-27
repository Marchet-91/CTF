#!/usr/bin/env python3

import os
from hashlib import sha256

flag = os.getenv('FLAG', 'CCIT{redacted}').encode()
iflag = int.from_bytes(flag)

while 1:
    pw = input('Password? ').encode()
    k = int.from_bytes(sha256(pw).digest())
    
    andc = (iflag & k).to_bytes(len(flag))
    print(f'Here\'s your andcrypted flag: {andc.hex()}')
