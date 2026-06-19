from factordb.factordb import FactorDB
from Crypto.Util.number import long_to_bytes

c = 15341890103764929939105506004034128738090325640037083301857608662849501626260517
n = 948406957756830799684818171639547165784816468744946013083947881743680617123566349
e = 65537

f = FactorDB(n)
f.connect()
p, q = f.get_factor_list()

fi = (p-1)*(q-1)
d = pow(e, -1, fi)
pt = long_to_bytes(pow(c, d, n)).decode()ls
cd[::-1]

print(pt)