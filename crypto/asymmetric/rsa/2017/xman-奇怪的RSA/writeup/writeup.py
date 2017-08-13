import gmpy2
import random
from Crypto.Util.number import getPrime
from Crypto.PublicKey import RSA


def get_part1(number):
    res = 1
    for i in range(2, number):
        j = 2
        flag = True
        while j * j <= i:
            if i % j == 0:
                flag = False
                break
            j += 1
        if flag:
            res *= i
    print res


def get_n_e():
    with open('./public.pem') as f:
        key = RSA.importKey(f)
        print 'n: ', key.n
        print 'e: ', key.e
    return key.n, key.e


def get_enc():
    with open('./flag.enc') as f:
        return int(f.read(), 16)


#get_part1(100)
n, e = get_n_e()
enc = get_enc()
p = 30912612430010329735106068745932328064975005191230456661938177099292739592747102255580455176474604978442049097442980075369740910342136464209806039144344258921430018016151786358282584701369623
q = 11639037836852113089565519736106317677116681989454609894239129622475886599564754669490030026817850279221814205531802378242845562976929460565098348616301827
phin = (p - 1) * (q - 1)
d = gmpy2.invert(e, phin)
flag = gmpy2.powmod(enc, d, n)
print hex(flag)[2:].decode('hex')
