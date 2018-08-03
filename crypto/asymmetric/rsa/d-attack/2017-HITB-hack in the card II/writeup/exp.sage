
def rsa(bits):
    # only prove correctness up to 1024 bits
    proof = (bits <= 1024)
    p = next_prime(ZZ.random_element(2**(bits//2+1)),
            proof=proof)
    q = next_prime(ZZ.random_element(2**(bits//2+1)),
            proof=proof)
    n = p*q
    phi_n = (p-1)*(q-1)
    while True:
        e = ZZ.random_element(1,phi_n)
        if gcd(e,phi_n) == 1: break
    d = lift(Mod(e,phi_n)^(-1))
    return e, d, n, p, q


def get_ed(p, q, e1):
    n = p*q
    phi_n = (p-1)*(q-1)
    while True:
        e2 = ZZ.random_element(1,phi_n)
        if gcd(e2,phi_n) == 1 and gcd(e1, e2) != 1: 
            break
    d2 = lift(Mod(e2,phi_n)^(-1))
    return e2, d2

def encrypt(m, e, n):
    return lift(Mod(m,n)^e)


def decrypt(c, d, n):
    return lift(Mod(c,n)^d) 


# solution a - take a long long time
def find_p(n, e, d):
    maxloops = e*d - 1
    p = 0
    k = 0
    while True:
        if k >= maxloops:
            print 'factorization failed...'
            break
        k += 1
        b = n - maxloops/k + 1
        if b in ZZ:
            f = x^2 - b*x + n
            try:
                p = find_root(f, 1,n)
            except Exception as e:
                pass
            if p and p in ZZ:
                print 'p = %d \nk = %d' % (p,k)
                break


# solution b - has a probability of 1/2
def find_q(n, e, d):
    phi_mod = e*d - 1
    i = 1
    tmp = phi_mod
    while True:
        tmp = phi_mod/2^i
        if is_odd(tmp):
            break
        i += 1
    while True:
        a = ZZ.random_element(n-2)
        if gcd(a,n) != 1:
            return gcd(a,n)
        a_tmp = a.powermod(tmp, n)
        if a_tmp.powermod(2, n) == 1:
            q = gcd(a_tmp+1, n)
            if q == n or q == 1:
                continue
            else:
                return q
