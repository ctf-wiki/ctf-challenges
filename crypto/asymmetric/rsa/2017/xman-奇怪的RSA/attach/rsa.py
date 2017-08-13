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
    tmp = random.randint(1000, 9999)
    return res + tmp


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


def encrypt():
    flag = open('./flag.txt').read().strip('\n')
    flag = flag.encode('hex')
    flag = int(flag, 16)
    with open('./public.pem') as f:
        key = RSA.importKey(f)
        enc = gmpy2.powmod(flag, key.e, key.n)
    with open('flag.enc', 'w') as f:
        f.write(hex(enc)[2:])


generate_public_key()
encrypt()
