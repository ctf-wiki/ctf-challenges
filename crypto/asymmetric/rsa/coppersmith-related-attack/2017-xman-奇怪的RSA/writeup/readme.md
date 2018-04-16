# 分析

首先，简单分析一下程序，可以知道程序利用generate_public_key函数生成RSA公钥，利用encrypt函数加密flag，最后将flag以十六进制形式输入到flag.enc文件中。这里我们来仔细看下生成公钥的函数。

```python
def generate_public_key():
    part1 = get_part1(100) << 512
    part2 = random.randrange(1, 2**256)
    p = part1 + part2
    while not gmpy2.is_prime(p):
        p = part1 + random.randrange(1, 2**256)
    q = getPrime(512)
    n = p * q
    e = 0x10001
    key = RSA.construct((long(n), long(e)))
    key = key.exportKey()
    with open('public.pem', 'w') as f:
        f.write(key)
```

可以看出，p是由两部分组成的，其中一部分是由get_part1函数左移512位得到。

```python
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
    tmp = random.randint(1000, 9999)
    return res + tmp
```

而get_part1函数其实就是讲100以内的素数乘起来然后再加上(1000,9999)的一个随机值。如果我们假设100以内的素数的乘积为a，那么get_part1的结果就是a+random(1000,9999)。

此后这个数会被移位，然后再加上了(1, 2**256)范围内的随机数。乍一看可能觉得不能做，，，但其实这道题是[Factoring with High Bits Known](https://ctf-wiki.github.io/ctf-wiki/#/crypto/asymmetric/rsa/rsa_coppersmith_attack?id=factoring-with-high-bits-known) 攻击，我们虽然说p的高位有一小部分是随机数，但是这部分随机数太小了，我们可以暴力枚举来得到结果。

# 代码

首先，我们先得到n和e，以及p的高位中100以内的素数的乘积

```python
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
```

然后我们可以直接编写sage代码得到p和q。

```python

from sage.all import *

n=359793065708835171342012982403389538721788606457645856715487227577194526064798303818572407032975833936178199713595331846778102841997912700946265231285246024230663051859876335242072374004279978008125992004515027281010928770488746000301666740722019469328342218484337725625411326416836525568083940937252398788555611188099231630860828419152057201221L

e = 65537L

part1 = 2305567963945518424753102147331756070

def high_bits_known(pbar):
    beta = 0.3
    kbits = 256
    PR.<x> = PolynomialRing(Zmod(n))
    f = x + pbar
    x0 = f.small_roots(X=2^kbits, beta=beta)
    return x0

for x in xrange(1000, 9999):
    if x % 100 == 0:
        print 'try ',x
    tmp = part1+x
    pbar = tmp*(2**512)
    p = high_bits_known(pbar)
    if len(p) > 0:
        p = ZZ(p[0] + pbar)
        if n % p == 0:
            print "!!!Found!!!"
            print "p: ",p
            print "q: ",n/p
```

下面，我们就可以对密文进行解密得到结果了

```python
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
```

具体更加详细的代码可以参考writeup.py以及exp.sage。