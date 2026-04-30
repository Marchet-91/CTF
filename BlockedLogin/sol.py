from pwn import * 

HOST = "blocked.challs.cyberchallenge.it"
PORT = 9214
BLOCK_SIZE=16

io = remote(HOST, PORT)
def pad(s): return s + (BLOCK_SIZE - len(s) %
                        BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

name = ""
assert(all(c in string.printable for c in name))
surname = ""
assert(all(c in string.printable for c in surname))
email = ""
assert(all(c in string.printable for c in email))

data = '{"name": "%s", "surname": "%s", "email": "%s", "type": "user"}' % (name, surname, email)

payload = ""

io.close()