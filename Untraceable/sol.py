KEY = "s3cret_k3y".encode()

with open("2.bin", "rb") as f:
    file = f.readlines()

pt = "".encode()
with open("forse.bin", "w") as f:
    for ct in file:
        for i in range(len(ct)):
            f.write(chr(ct[i] ^ KEY[i % len(KEY)]))
        # print()
    # print()

# print(pt)