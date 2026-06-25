from factordb.factordb import FactorDB
from Crypto.Util.number import long_to_bytes

n = 8749002899132047699790752490331099938058737706735201354674975134719667510377522805717156720453193651
e = 65537
ct = 6922480675050049607722767919273094265169824930313752450528383444577397545413062855020890103021658446


f = FactorDB(n)
f.connect()
fat = f.get_factor_list()
fi = 1
for i in fat: 
    fi *= (i-1)

d = pow(e, -1, fi)

print(long_to_bytes(pow(ct, d, n)).decode())