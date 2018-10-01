#!/usr/bin/env python3.6
import os

BLOCK_SIZE = 64

T = [
    ((2, 1), 1),
    ((5, 0), 0),
    ((3, 4), 0),
    ((1, 5), 1),
    ((0, 3), 1),
    ((4, 2), 0),
]


def block2bin(b, length=BLOCK_SIZE):
    return list(map(int, bin(b)[2:].rjust(length, '0')))


def bin2block(b):
    return int("".join(map(str, b)), 2)


def transduce_iter(b, s=0):
    ans = []
    for c in b:
        d, t = T[s]
        ans += [c ^ t]
        s = d[c]
    return ans


def transduce(b, s=0):
    if len(b) == 0:
        return b
    d, t = T[s]
    b0, bp = b[0], b[1:]
    return [b0 ^ t] + transduce(bp, s=d[b0])


def transduceblock(b):
    return bin2block(transduce(block2bin(b)))


def swap(b):
    l = BLOCK_SIZE // 2
    m = (1 << l) - 1
    return (b >> l) | ((b & m) << l)


class Transducipher:

    def __init__(self, k):
        self.k = [k]
        for i in range(1, len(T)):
            k = swap(transduceblock(k))
            self.k.append(k)

    def encrypt(self, b):
        for i in range(len(T)):
            b ^= self.k[i]
            b = transduceblock(b)
            b = swap(b)
        return b


if __name__ == "__main__":
    flag = bytes.hex(os.urandom(BLOCK_SIZE // 8))
    k = int(flag, 16)
    C = Transducipher(k)
    print("Your flag is PCTF{%s}" % flag)
    with open("data1.txt", "w") as f:
        for i in range(16):
            pt = int(bytes.hex(os.urandom(BLOCK_SIZE // 8)), 16)
            ct = C.encrypt(pt)
            f.write(str((pt, ct)) + "\n")
