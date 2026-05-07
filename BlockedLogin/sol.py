from pwn import * 
import json

HOST = "blocked.challs.cyberchallenge.it"
PORT = 9214
BLOCK_SIZE=16

# io = remote(HOST, PORT)
def pad(s): return s + (BLOCK_SIZE - len(s) %
                        BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def unpad(s): return s[:-ord(s[len(s) - 1:])]

name = "ciaoaaaaaaaaaaaaaaaa"
assert(all(c in string.printable for c in name))
surname = "admin"
assert(all(c in string.printable for c in surname))
email = 'abo'
assert(all(c in string.printable for c in email))

data = '{"name": "%s", "surname": "%s", "email": "%s", "type": "user"}' % (name, surname, email)

data = json.dumps(json.loads(data))
print(pad(data).encode())


print("\n\n\n")

block = []
# print(data[0:0+16])
for i in range(0,len(data),16):
    block.append(data[i:i+16])

for i in block:
    print(i)

# io.close()