from Crypto.Hash import SHA
from pwn import *
import gmpy2
from gmpy2 import is_prime
import random


def PKCS1_pad(data):
    asn1 = "3021300906052b0e03021a05000414"
    ans = asn1 + data
    n = len(ans)
    return int(('00' + '01' + 'ff' * (1024 / 8 - n / 2 - 3) + '00' + ans), 16)


#context.log_level = 'debug'
def gen_smooth_num(plist, minnum=pow(2, 1020)):
    lenp = len(plist)
    while True:
        n = 1
        factors = dict()
        while n + 1 < minnum:
            tmp = random.randint(0, lenp - 1)
            n *= plist[tmp]
            if plist[tmp] in factors:
                factors[plist[tmp]] += 1
            else:
                factors[plist[tmp]] = 1
        if n.bit_length() > 1024:
            continue
        if is_prime(n + 1):
            return n + 1, factors


# http://pythonexample.com/snippet/pohligpy_neuratron_python
# solve g^x=h mod m
def log_prime_power(g, h, pf, pe, M):

    powers = [pf**k for k in range(pe)]

    gamma = gmpy2.powmod(g, powers[-1], M)

    xk = gmpy2.mpz(0)
    for k in range(pe):
        if k == 0:
            hk = gmpy2.powmod(h, powers[pe - k - 1], M)
        else:
            gk = gmpy2.powmod(g, xk * (M - 2), M)
            hk = gmpy2.powmod(gk * h, powers[pe - k - 1], M)

        k_log_found = False
        for dk in range(pf):
            yk = gmpy2.powmod(gamma, dk, M)
            if yk == hk:
                k_log_found = True
                break

        if not k_log_found:
            raise Exception("can not solve")

        xk += gmpy2.mul(powers[k], dk)

    return xk


def pohlig_hellman(g, h, M, factors):
    M1 = M - 1
    xs = []
    for f in factors:
        pf = f
        pe = factors[f]

        subgroup_exponent = gmpy2.div(M1, gmpy2.powmod(pf, pe, M))
        gi = gmpy2.powmod(g, subgroup_exponent, M)
        hi = gmpy2.powmod(h, subgroup_exponent, M)

        xi = log_prime_power(gi, hi, pf, pe, M)
        xs.append(xi)
    crt_coeffs = []

    for f in factors:
        pf = f
        pe = factors[f]

        mi = pf**pe

        bi = gmpy2.div(M, mi)
        bi_inv = gmpy2.invert(bi, mi)
        crt_coeffs.append(gmpy2.mul(bi, bi_inv))
    x = 0
    for i in range(len(crt_coeffs)):
        x = gmpy2.t_mod(x + gmpy2.t_mod(xs[i] * crt_coeffs[i], M1), M1)
    return x


#context.log_level = 'debug'


def main():
    port = 12345
    host = "127.0.0.1"
    p = remote(host, port)
    p.recvuntil('Message   -> ')
    message = p.recvuntil('\n\nSignature -> ', drop=True)
    log.info('message: ' + message)
    signature = p.recvuntil('\n', drop=True)
    log.info('signature: ' + signature)
    signature = int(signature, 16)
    h = SHA.new(message)

    m = PKCS1_pad(h.hexdigest())
    print m, signature
    plist = []
    for i in range(2, 1000):
        if is_prime(i):
            plist.append(i)
    while True:
        try:
            n, factors = gen_smooth_num(plist, signature)
            e = pohlig_hellman(signature, m, n, factors)
        except Exception as e:
            continue
        else:
            break
    print n, e

    print m
    print gmpy2.powmod(signature, e, n)

    p.sendlineafter('Enter n:', str(n))
    p.sendlineafter('Enter e:', str(e))

    p.interactive()


main()
