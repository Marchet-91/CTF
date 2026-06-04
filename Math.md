# SAGEMATH
## tipi
- MOD(n1, n2): converte un numero intero in un elemento dell'anello Z/nZ (interi modulo n).
- ordine di elemento g: è il numero più picolo positivio n tale che g^n = 1 (mod p), ris: n

## operazioni
- val.log(base): devono essere dello stesso tipo val e base

# MATH
- pow(a, (p - 1) // 2, p) = 1: a ha una radice quadrata
                          = p-1: a non ha una radice quadrata
                          = 0: a è divisibile per p
- Se quello sopra è vero allora per calcolare la radice quadrata fai:
     pow(a, (p + 1) // 4, p)

- a^p = p (mod p) && gcd(a, p) = 1 allora a^(p - 1) = 1 (mod p) 