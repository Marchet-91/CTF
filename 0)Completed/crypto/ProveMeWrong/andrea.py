from random import SystemRandom
from operator import lshift
import math
from Crypto.Util.number import long_to_bytes

random = SystemRandom()
nbits = 256

risultato = round(15 * 0.666)

print(risultato)

sample = sorted(random.sample(range(nbits), k=15))

print(sample)

def incrementare(n):
 return n + 1
numeri1 = (0, 1, 2, 3, 4)
numeri2 = (1, 1, 1, 1, 1)

print(lshift(2,1))

risultato = sum(map(lshift, numeri1,numeri2))
srdnlen = b"we are srdnlen!"

# come ho scritto in chall posso riscriverlo come:
# n = p * (p + x *sum)
# n = p^2 + p*x*sum 
# per trovare p è quindi un'equazione di secondo grado  p^2 + p*x*sum + n = 0 con:
# a = 1
# b = x*sum
# c = n
# p = (-b +- sqrt(b^2 - 4ac)) / 2a # però prendo la soluzione positiva
# in realtà b^2 - 4ac non può essere negativo altrimenti non is può fare la radice quadrata quindi dovrò
# controllare prima che delta sia positivo

# quindi risolvo questa equazione con il sample che sto bruteforceando e mi calcolo q phi e d
# poi mando il decrypt e se srdnlen{ è nel risultato allora è giusta e fermo tutto

sample = [18, 32, ..., ..., 130, 138, 145, ..., 180, 183, 189, 205, 221, ..., ...]

# devo bruteforcare il sample giusto

a = 1

n = 3939930432607568271028006178835273343365969273890011029334148059968112291984800526003772464130883943191723987350327352277647934827274472714706501384053753

c = n

e = 0x10001

flag_enc = 2869429344439206906531588120924725691313414493116437092996652346479439780409533002845413737504581129739595694725033319847726785183127845067606127237223702

for first in range(34,130):

#  print(f"Sono vivo")

 for second in range(first + 1, 130):

#   print(f"Sono quasi vivo")

  for third in range(145,180):

   for fourth in range(221,256):

    for fifth in range(fourth + 1,256):
     
     sample_try = [18, 32, first, second, 130, 138, 145, third, 180, 183, 189, 205, 221, fourth, fifth]
     print(sample_try)
     b = sum(map(lshift, srdnlen, sample_try))

     delta = b**2 - 4*a*(-c)

     # se è minore di zero continuo allora cambio giro del ciclio con continue (è piu ottimizzato)

     if delta <= 0:

      continue

     # controllo che la radice sia un intero
     square = math.sqrt(delta)
     
     if int(square) == square:
      
      # non posso avere float quindi faccio //
      p = (-b + int(square)) // 2*a

      # non posso avere float quindi faccio //
      q = n // p

      phi = (p-1)*(q-1)

      try:
       d = pow(e, -1, phi)
      except ValueError as error:
       pass

      decryption = long_to_bytes(pow(flag_enc, d, n))

      if b'srdnlen{' in decryption:

       log.succes(f"Flag: {decryption}")
       exit()