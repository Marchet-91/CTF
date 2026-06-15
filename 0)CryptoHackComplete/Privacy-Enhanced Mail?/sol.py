from Crypto.PublicKey import RSA

f = RSA.import_key(open("privacy_enhanced_mail.pem").read())

print(f.d)