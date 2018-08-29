#!/usr/bin/env python3.6
import os
import itertools
BLOCK_SIZE = 32

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


def transduce(b, s=0):
    if len(b) == 0:
        return b
    d, t = T[s]
    b0, bp = b[0], b[1:]
    return [b0 ^ t] + transduce(bp, s=d[b0])


def transduceblock(b, s=0):
    return bin2block(transduce(block2bin(b), s))


def invtransduce(b, s=0):
    if len(b) == 0:
        return b
    d, t = T[s]
    b0, bp = b[0], b[1:]
    return [b0 ^ t] + transduce(bp, s=d[b0 ^ t])


def invtransduceblock(b):
    return bin2block(invtransduce(block2bin(b)))


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


p_c = []


def transduce_iter(b, s=0):
    ans = []
    #idx = 0
    for c in b:
        d, t = T[s]
        ans += [c ^ t]
        s = d[c]
        # print idx, s
        idx += 1
    return s


def brute_right(plain, cipher, left_32):
    all_candidate = []
    for st in range(pow(6, 5)):
        states = [(st // (6**j)) % 6 for j in range(5)]
        #print states
        candidate = [0]
        for i in range(32):
            new_candidate = []
            for c, bit in itertools.product(candidate, range(2)):
                #print c, bit
                k_i = (c << 1) + bit
                k_now = k_i << (32 - i - 1)
                key = [k_now]
                k = block2bin(k_now, 32)
                # get all key
                for j in range(1, 6):
                    if j == 1:
                        k = transduce(k, left_32)
                    elif j % 2 == 1:
                        # 3 for 1
                        # 5 for 2
                        k = transduce(k, states[(j >> 1) - 1])
                    else:
                        k = transduce(k, 0)
                    key.append(bin2block(k))
                flag = True
                # encrypt message
                data = plain
                for k in range(6):
                    if k == 0:
                        data = transduceblock(data ^ key[k], states[2])
                    elif k == 2:
                        data = transduceblock(data ^ key[k], states[3])
                    elif k == 4:
                        data = transduceblock(data ^ key[k], states[4])
                    else:
                        data = transduceblock(data ^ key[k], 0)
                if (data >> (32 - i - 1)) == (cipher >> (32 - i - 1)):
                    new_candidate.append(k_i)
                    #print 'one'
            candidate = new_candidate
            if len(new_candidate) == 0:
                break
        for k in candidate:
            if k not in all_candidate:
                all_candidate.append(k)
        print st, len(all_candidate)
    return all_candidate


def brute_left(plain, cipher):
    all_candidate = []
    for st in range(pow(6, 5)):
        states = [(st // (6**j)) % 6 for j in range(5)]
        #print states
        candidate = [0]
        for i in range(32):
            new_candidate = []
            for c, bit in itertools.product(candidate, range(2)):
                #print c, bit
                k_i = (c << 1) + bit
                k_now = k_i << (32 - i - 1)
                key = [k_now]
                k = block2bin(k_now, 32)
                # get all key
                for j in range(1, 6):
                    if j == 2:
                        k = transduce(k, states[0])
                    elif j == 4:
                        k = transduce(k, states[1])
                    else:
                        k = transduce(k, 0)
                    key.append(bin2block(k))
                flag = True
                # encrypt message
                data = plain
                for k in range(6):
                    if k == 1:
                        data = transduceblock(data ^ key[k], states[2])
                    elif k == 3:
                        data = transduceblock(data ^ key[k], states[3])
                    elif k == 5:
                        data = transduceblock(data ^ key[k], states[4])
                    else:
                        data = transduceblock(data ^ key[k], 0)
                if (data >> (32 - i - 1)) == (cipher >> (32 - i - 1)):
                    new_candidate.append(k_i)
                    #print 'one'
            candidate = new_candidate
            if len(new_candidate) == 0:
                break
        for k in candidate:
            if k not in all_candidate:
                all_candidate.append(k)
        print st, len(all_candidate)
    return all_candidate


def get_left_key():
    left_key = []
    for i in range(0, len(p_c)):
        plain = p_c[i][0] >> 32
        cipher = p_c[i][1] >> 32
        possible = brute_left(plain, cipher)
        new_key = []
        if len(left_key) == 0:
            left_key = possible
        else:
            for j in left_key:
                if j in possible:
                    new_key.append(j)
            left_key = new_key
        print left_key, len(left_key)
        # stop it and see
        raw_input()


def get_right_key(left_32):
    right_key = []
    for i in range(0, len(p_c)):
        plain = p_c[i][0] & 0xffffffff
        cipher = p_c[i][1] & 0xffffffff
        print plain, cipher
        possible = brute_right(plain, cipher, left_32)
        new_key = []
        if len(right_key) == 0:
            right_key = possible
        else:
            for j in right_key:
                if j in possible:
                    new_key.append(j)
            right_key = new_key
        # stop it and see
        print right_key, len(right_key)
        raw_input()


if __name__ == "__main__":
    s = open('./data.txt').read().strip()
    s = s.split('\n')
    p_c = map(eval, s)
    # get_left_key()
    left_key = [2659900894, 2659900895]
    for left in left_key:
        left = block2bin(left)
        fs = transduce_iter(left)
        print fs
        get_right_key(fs)
