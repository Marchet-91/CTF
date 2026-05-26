from pwn import *
import math

def get_n_and_e(io):
    # Ask for encryption of 2 and 4
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Plaintext > ', b'2')
    io.recvline()
    # print(io.recvline().split(b" "))
    c2 = int(io.recvline().strip().split(b" ")[-1])
    
    io.sendlineafter(b'> ', b'1')
    # print(io.recvline())
    io.sendlineafter(b'Plaintext > ', b'4')
    # print("ciao")
    io.recvline()
    c4 = int(io.recvline().strip().split(b" ")[-1])
    # print("ciao")

    # n divides c2^2 - c4
    k1 = c2*c2 - c4
    
    # Ask for encryption of 3 and 9
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Plaintext > ', b'3')
    io.recvline()
    c3 = int(io.recvline().strip().split(b" ")[-1])
    
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'Plaintext > ', b'9')
    io.recvline()
    c9 = int(io.recvline().strip().split(b" ")[-1])
    
    k2 = c3*c3 - c9
    
    n = math.gcd(k1, k2)
    
    # find e
    for e in [65537, 3, 17]:
        if pow(2, e, n) == c2:
            return n, e
    
    raise ValueError("e not found")

def attack(io, n, e, flag_encrypted):
    r = 2
    # encrypt r
    c_r = pow(r, e, n)
    c_prime = (flag_encrypted * c_r) % n
    
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'Ciphertext > ', str(c_prime).encode())
    print(io.recvline())
    m_prime = int(io.recvline().split()[-1])
    
    # Try both possibilities
    for candidate in [m_prime // r, (m_prime + n) // r]:
        if pow(candidate, e, n) == flag_encrypted:
            return candidate
    
    return None

def main():
    # Connect to the service (example: netcat localhost 1234)
    # Replace with actual host/port
    io = remote('oracle.challs.cyberchallenge.it', 9041)
    
    io.recvuntil(b'Encrypted flag:')
    flag_encrypted = int(io.recvline().strip())
    
    n, e = get_n_and_e(io)
    print(f"n = {n}\ne = {e}")
    
    flag_int = attack(io, n, e, flag_encrypted)
    flag = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, 'big')
    print("FLAG:", flag)
    
    io.close()

if __name__ == '__main__':
    main()