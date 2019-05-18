#!/usr/bin/env python

import hashlib
import hmac
import marshal
import signal
import sys
import time
import types

try:
    from Crypto.Util import number
except ImportError:
    pass

TIMEOUT = 940
NCHALLENGES = 3
NSIZE = 1280


def create_key():
    Nsize = NSIZE
    pqsize = Nsize / 2
    N = 0
    while N.bit_length() != Nsize:
        while True:
            p = number.getStrongPrime(pqsize)
            q = number.getStrongPrime(pqsize)
            if abs(p - q).bit_length() > Nsize * 0.496:
                break

        N = p * q

    phi = (p - 1) * (q - 1)
    limit1 = 0.261
    limit2 = 0.293
    while True:
        d = number.getRandomRange(
            pow(2, int(Nsize * limit1)), pow(2,
                                             int(Nsize * limit1) + 1)
        )
        while d.bit_length() < Nsize * limit2:
            ppp = 0
            while not number.isPrime(ppp):
                ppp = number.getRandomRange(pow(2, 45), pow(2, 45) + pow(2, 12))
            print(ppp)
            d *= ppp

        if number.GCD(d, phi) != 1:
            continue
        e = number.inverse(d, phi)
        if number.GCD(e, phi) != 1:
            continue
        break
    print(e, d, N)

    zzz = 3
    return (N, e)


create_key()
exit(0)
