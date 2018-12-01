from pwn import *
import gmpy2
from fractions import Fraction
p = process('./rsa.py')
#p = remote('18.179.251.168', 21700)
#context.log_level = 'debug'
p.recvuntil('Here is the flag!\n')
flagcipher = int(p.recvuntil('\n', drop=True), 16)


def long_to_hex(n):
    s = hex(n)[2:].rstrip('L')
    if len(s) % 2: s = '0' + s
    return s


def send(ch, num):
    p.sendlineafter('cmd: ', ch)
    p.sendlineafter('input: ', long_to_hex(num))
    data = p.recvuntil('\n')
    return int(data, 16)


if __name__ == "__main__":
    # get n
    cipher2 = send('A', 2)
    cipher4 = send('A', 4)
    nset = []
    nset.append(cipher2 * cipher2 - cipher4)

    cipher3 = send('A', 3)
    cipher9 = send('A', 9)
    nset.append(cipher3 * cipher3 - cipher9)
    cipher5 = send('A', 5)
    cipher25 = send('A', 25)
    nset.append(cipher5 * cipher5 - cipher25)
    n = nset[0]
    for item in nset:
        n = gmpy2.gcd(item, n)

    # get map between k and return byte
    submap = {}
    for i in range(0, 256):
        submap[-n * i % 256] = i

    # get cipher256
    cipher256 = send('A', 256)

    back = flagcipher

    L = Fraction(0, 1)
    R = Fraction(1, 1)
    for i in range(128):
        print i
        flagcipher = flagcipher * cipher256 % n
        b = send('B', flagcipher)
        k = submap[b]
        L, R = L + (R - L) * Fraction(k, 256
                                     ), L + (R - L) * Fraction(k + 1, 256)
    low = int(L * n)
    print long_to_hex(low - low % 256 + send('B', back)).decode('hex')
