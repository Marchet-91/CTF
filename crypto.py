def euclideo(a, b):
    while b != 0:
        t = b
        b =  a % b
        a = t
    return a

def euclideo_ext(a,b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    return a, x0, y0

def ceaser(i, ct):
    pt = ""
    for j in range(len(ct)):
        if ct[j] >= 'A' and ct[j] <= 'Z':
            pt += chr((ord(ct[j]) - ord('A') - i) % 26 + ord('A'))
            # print(pt)
        elif ct[j] >= 'a' and ct[j] <= 'z':
            pt += chr((ord(ct[j]) - ord('a') - i) % 26 + ord('a'))
        else:
            pt += ct[j]
    return pt



# conda activate venvCrypto