from PIL import Image
from pwn import xor

img1 = Image.open("lemur_ed66878c338e662d3473f0d98eedbd0d.png").convert("RGB")
img2 = Image.open("flag_7ae18c704272532658c10b5faad06d74.png").convert("RGB")

# stessa size
if img1.size != img2.size:
    raise ValueError("Le immagini devono avere la stessa dimensione")

# stream RGB raw
b1 = img1.tobytes()
b2 = img2.tobytes()

# XOR byte-to-byte
xored = xor(b1, b2)

# ricostruisci immagine
out = Image.frombytes("RGB", img1.size, xored)

out.save("new.png")
out.show()

# crypto{X0Rly_n0t!}