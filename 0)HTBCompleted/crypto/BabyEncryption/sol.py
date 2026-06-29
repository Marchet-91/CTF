ct = open("msg.enc", "r").readline()
ct = bytes.fromhex(ct)

d = pow(123, -1, 256)
pt = b""
for c in ct: 
    pt += (((c - 18) * d) % 256).to_bytes()

print(pt.decode())