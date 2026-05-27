# PYTHON
- prob = {
    'a': 0.082, 'b': 0.015, 'c': 0.028, 'd': 0.043, 'e': 0.127, 'f': 0.022, 'g': 0.020, 
    'h': 0.061, 'i': 0.070, 'j': 0.002, 'k': 0.008, 'l': 0.040, 'm': 0.024, 'n': 0.067, 
    'o': 0.075, 'p': 0.019, 'q': 0.001, 'r': 0.060, 's': 0.063, 't': 0.091, 'u': 0.028, 
    'v': 0.010, 'w': 0.023, 'x': 0.001, 'y': 0.020, 'z': 0.001
}

- L'inverso di int.from_bytes(, "big"):
    back = n.to_bytes((n.bit_length() + 7) // 8, "big")

# WEB
- ${IFS}: per mettere lo spazio senza metterlo in terminale
    wget${IFS}--post-file${IFS}<file>${IFS}<site>

# PWN
## pwninit:
sudo /home/rosi/Projects/CTF/pwninit --no-template --bin=<binario> --libc=<libreria> --ld=<loader>

# CRYPTO
- find iv having ct or find key, having ct prev with plaintext:
    cat /home/rosi/Projects/CTF/0\)Completed/crypto/Redacted/sol.py

- quando si fa lo xor tra le due immagini, il risultato sarà la differenza più o meno, quidi notterai le differenze tra i due

- quadratic residuo:
        Quadratic Residue * Quadratic Residue = Quadratic Residue
        Quadratic Residue * Quadratic Non-residue = Quadratic Non-residue
        Quadratic Non-residue * Quadratic Non-residue = Quadratic Residue 

- RSA vuln:
    - small public modulus: fattorizzabile
    - when e is small, and ct, is smaller than n: iroot of ct^e
    - common modulo: quando abbiamo moduli uguali ma espontenti diversi, possiamo ricavare n con gcd dalla ct
    - avere common modulo: possiamo cifrare 2 e 4, e quindi alla fine risultera che le due cifrazionia avranno e diverso ma n uguale;

- ricavare la e:
    - provare e comuni
    - usare il teorema di eulero: 

- RSA Properties:
    - encrypt(a * b) = encrypt(a) * encrypt(b)
    - decrypted(flag * b) = flag * b (mod n):
        - flag = (decrypted(flag * b) / b)      flag * r >= n
        - flag =  m // b                        flag * r < n

- Controllare la funzione che si usa per generare i numeri

# SYSCALL
- execve:
    rax: 59
    rdi: command
    rsi: 0
    rdx: 0