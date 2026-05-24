import numpy as np
from PIL import Image

im1 = Image.open("flag_enc.png")
im2 = Image.open("notflag_enc.png")

im1np = np.array(im1)*255
print(im1np)

# f = img2 ^ k
# nf = img1 ^ k
# img2 ^ h1 = img1 ^ h2
# k = img2 ^ h1
# k = img1 ^ h2
                    
