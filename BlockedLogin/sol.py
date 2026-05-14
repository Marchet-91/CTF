from pwn import * 
import json

HOST = "blocked.challs.cyberchallenge.it"
PORT = 9214
BLOCK_SIZE=16

# io = remote(HOST, PORT)
def pad(s): return s + (BLOCK_SIZE - len(s) %
                        BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

def unpad(s): return s[:-ord(s[len(s) - 1:])]

name = 'aAAA", "type": "admin", "x": "'
assert(all(c in string.printable for c in name))
surname = 'b'
assert(all(c in string.printable for c in surname))
email = 'C"}, {"Ciao'
assert(all(c in string.printable for c in email))

data = '{"name": "%s", "surname": "%s", "email": "%s", "type": "user"}' % (name, surname, email)
print(data)
data = json.dumps(json.loads(data))

for i in range(0, len(data), 16):
    print(data[i:i +16])
print(pad(data).encode())


io = remote(HOST, PORT)

io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"name: ", name.encode())
io.sendlineafter(b"surname: ", surname.encode())
io.sendlineafter(b"email: ", email.encode())
io.recvline()
token = io.recvline().strip()

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b": ", token)

print(io.recvline())
print(io.recvline())

io.close()