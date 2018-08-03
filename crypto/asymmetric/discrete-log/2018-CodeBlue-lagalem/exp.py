import gmpy2
data = open('./transcript.txt').read().split('\n')
print eval(data[0])
g, h, A, B, p, q = eval(data[0])

c1, c2 = eval(data[1])
c1_, c2_ = eval(data[2])

tmp = gmpy2.powmod(c2, A, p) * gmpy2.powmod(h, B, p) * gmpy2.invert(c2_, p)
tmp = tmp % p
print gmpy2.gcd(A - 1, p)

print 't=', tmp
print 'A=', A
print 'p=', p
gg, x, y = gmpy2.gcdext(A - 1, p - 1)
print gg

m = gmpy2.powmod(tmp, x, p)
print hex(m)[2:].decode('hex')
