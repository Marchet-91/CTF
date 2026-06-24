from PIL import Image
from PIL.ExifTags import TAGS
from Crypto.PublicKey import RSA 
from Crypto.Util.number import long_to_bytes, bytes_to_long

img = Image.open("image.jpg")

exif_data = img.info

key = exif_data["comment"]

RSA_KEY = bytes.fromhex(key.decode())

key = RSA.import_key(RSA_KEY)

ct = open("flag.enc", "rb").readline()
print(long_to_bytes(pow(bytes_to_long(ct), key.d, key.n)))