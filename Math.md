# SAGEMATH

## tipi

- MOD(n1, n2): converte un numero intero in un elemento dell'anello Z/nZ (interi modulo n).
- ordine di elemento g: è il numero più picolo positivio n tale che g^n = 1 (mod p), ris: n

## operazioni

- val.log(base): devono essere dello stesso tipo val e base

# SYMPY

- sqrt_mod(a, p, all_roots=True) = [max, min]
- crt(moduli, resti) = x: valore comune
  m: modulo totale

# MATH

- pow(a, (p - 1) // 2, p) = 1: a ha una radice quadrata
  = p-1: a non ha una radice quadrata
  = 0: a è divisibile per p
- Se quello sopra è vero allora per calcolare la radice quadrata fai and p = 3 (mod 4):
  pow(a, (p + 1) // 4, p)
- a^p = p (mod p) && gcd(a, p) = 1 allora a^(p - 1) = 1 (mod p)

### Probabilitstica

- quando due eventi sono legati bisogna usare moltiplicazione, mentre quando sono slegati bisogna usare addizione

