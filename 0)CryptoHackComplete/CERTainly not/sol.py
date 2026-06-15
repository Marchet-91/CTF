from Crypto.PublicKey import RSA

f = RSA.import_key(open("2048b-rsa-example-cert.der", "rb").read())

print(f.n)