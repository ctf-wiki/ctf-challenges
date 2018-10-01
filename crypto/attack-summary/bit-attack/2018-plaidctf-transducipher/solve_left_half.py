#!/usr/bin/env python
# coding=utf-8

from transducipher import transduce, rtransduce, bin2block, block2bin, Transducipher, T

def gets(bs):
    s = 0
    for i in bs:
        s = T[s][0][i]
    return s

def genk1(k, s):
    res = [k]
    tmp = k
    tmp = transduce(tmp)
    res.append(tmp)
    tmp = transduce(tmp, s)
    res.append(tmp)
    # print 'k1', res
    return res

def genk2(k, s):
    res = [k]
    tmp = k
    tmp = rtransduce(tmp)
    res += [tmp]
    tmp = rtransduce(tmp, s)
    res += [tmp]
    return res

def xor(a, b):
    assert len(a) == len(b)
    return [i^j for i,j in zip(a,b)]

def mid1(p, k, s0):
    for i in range(3):
        s = 0
        p = xor(p, k[i])
        if i == 1:
            s = s0
        p = transduce(p, s)
    res = bin2block(p)
    # print res
    return res

def mid2(p, k, s0, s1):
    for i in range(3):
        s = s0
        if i == 1:
            s = 0
        elif i == 2:
            s = s1
        p = rtransduce(p, s)
        p = xor(p, k[i])
    res = bin2block(p)
    # print res
    return res




n = 11 # 11+11+10=32

def solve(ct, pt, kk1, kk2):
    global mk1, mk2
    # print kk1, kk2
    # global kk1, kk2, key
    tmp_mk1 = []
    tmp_mk2 = []
    testp = map(lambda x: block2bin(x)[:len(kk1[0])+n], pt)
    testc = map(lambda x: block2bin(x)[:len(kk2[0])+n], ct)

    m = {}
    for ind, k2 in enumerate(mk2):
        if k2 is None:
            # print 'well'
            continue
        for i in range(6):
            for j in range(6):
                mid = map(lambda x: mid2(x, k2, i, j), testc)
                mid = tuple(mid)
                if m.has_key(mid):
                    m[mid].append((k2, i, j, ind))
                else:
                    m[mid] = [(k2, i, j, ind)]
                # if k2 == kkk2:
                #     print 'k2', mid

    print 'm OK', len(m)

    cnt = 0
    for ind, k1 in enumerate(mk1):
        if k1 is None:
            continue
        for i in range(6):
            mid = map(lambda x: mid1(x, k1, i), testp)
            mid = tuple(mid)
            # if k1 == kkk1:
            #     print 'k1', mid
            if m.has_key(mid):
                if k1[0] == [0] * 8:
                    # print 'k1', k1
                    # print 'k2', k2
                    pass
                for k2, ii, jj, ind2 in m[mid]:
                    if transduce(k1[-1]) == k2[-1]:
                        tmp_mk1.append((k1, ind))
                        tmp_mk2.append((k2, ind2))
                        cnt += 1
                        # print k1, i, k2, ii, jj
                        # break
    print 'filter mk', len(tmp_mk1), len(tmp_mk2)
    '''
    assert [i for i in tmp_mk1 if i[0] == kk1]
    assert [i for i in tmp_mk2 if i[0] == kk2]
    print 'pass assert!'
    '''
    mk1 = [None] * 6 * (2**n)
    mk2 = [None] * 6 * (2**n)
    for k1, ind1 in tmp_mk1:
        mk1[ind1] = k1
    for k2, ind2 in tmp_mk2:
        mk2[ind2] = k2
    print len([i for i in mk1 if i is not None]), len([i for i in mk2 if i is not None])

f = open('./data.txt')
pts = []
cts = []
for _ in range(16):
    pt, ct = eval(f.readline().strip())
    pts.append(pt)
    cts.append(ct)
f.close()
mk1 = None
mk2 = None
def final(kk1, kk2):
    print 'solve'
    print kk1
    print kk2
    global mk1, mk2
    mk1 = [None] * 6 * (2**n)
    mk2 = [None] * 6 * (2**n)
    for k in xrange(2**n):
        kb = block2bin(k)[-n:]
        for i in range(6):
            mk1[6*k+i] = genk1(kk1[0]+kb, i)
            mk2[6*k+i] = genk2(kk2[0]+kb, i)
    print 'mk OK'

    # import os
    # c = Transducipher(0)
    for i in range(16):
        # pt = int(os.urandom(8).encode('hex'), 16); ct = c.encrypt(pt) # for local debug
        solve(cts[i:i+1], pts[i:i+1], kk1, kk2)
        # solve([ct], [pt], kk1, kk2)
    return [i for i in mk1 if i is not None] + [i for i in mk2 if i is not None]

kk1 = [[], [], []]; kk2 = [[], [], []]; queue = [(kk1, kk2)]
# kk1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1]]; kk2 = [[0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0], [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]]; queue = [(kk1, kk2)]
# queue = [([[1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1]], [[1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1]]), ([[1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0]], [[1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0]])]
'''
queue = [([[1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
   [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
   [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
  [[1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
   [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
   [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]]),
 ([[1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1],
   [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
   [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]],
  [[1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
   [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
   [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0]])]
# '''
cnt = 0
while queue:
    cnt += 1
    kk1, kk2 = queue.pop(0)
    res = final(kk1, kk2)
    if res:
        print 'HAHA!'
        k1a, k1b, k2a, k2b = res
        print k1a
        print k2a
        print k1b
        print k2b
        if transduce(k1a[-1]) == k2b[-1]:
            queue.append((k1a, k2b))
            queue.append((k1b, k2a))
        else:
            queue.append((k1a, k2a))
            queue.append((k1b, k2b))
    if cnt == 10:
        break
print queue
