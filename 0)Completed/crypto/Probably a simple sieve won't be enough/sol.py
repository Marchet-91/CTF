from factordb.factordb import FactorDB
from Crypto.Util.number import long_to_bytes

c1 = 6513402340379073542230710001434049959082564276254477896792619
c2 = 2739603094136133383923409703861575117091198809308633380325460

n=9565158649535229609530047362785645907094563351070470563788237
e=65537

f = FactorDB(n)
f.connect()

p, q = f.get_factor_list()
fi = (p-1) * (q-1)
d = pow(e, -1, fi)

c1, c2 = pow(c1, d, n), pow(c2, d, n)

ct = hex(c1)[2:] + hex(c2)[2:]
print(bytes.fromhex(ct).decode())
