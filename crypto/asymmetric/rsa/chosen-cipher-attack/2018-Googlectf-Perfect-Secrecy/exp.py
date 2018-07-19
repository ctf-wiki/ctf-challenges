import gmpy2
from pwn import *
encflag = open('./flag.txt').read()
encflag = encflag.encode('hex')
encflag = int(encflag, 16)
#context.log_level = 'debug'
m = ['\x00', '\x07']
n = 0xDA53A899D5573091AF6CC9C9A9FC315F76402C8970BBB1986BFE8E29CED12D0ADF61B21D6C281CCBF2EFED79AA7DD23A2776B03503B1AF354E35BF58C91DB7D7C62F6B92C918C90B68859C77CAE9FDB314F82490A0D6B50C5DC85F5C92A6FDF19716AC8451EFE8BBDF488AE098A7C76ADD2599F2CA642073AFA20D143AF403D1
e = 65537
flag = ""


def guessvalue(cnt):
    if cnt[0] > cnt[1]:
        return 0
    return 1


i = 0
while True:
    cnt = dict()
    cnt[0] = cnt[1] = 0
    p = remote('perfect-secrecy.ctfcompetition.com', 1337)
    p.send(m[0])
    p.send(m[1])
    tmp = pow(2, i)
    two_inv = gmpy2.invert(tmp, n)
    two_cipher = gmpy2.powmod(two_inv, e, n)
    tmp = encflag * two_cipher % n
    tmp = hex(tmp)[2:].strip('L')
    tmp = '0' * (256 - len(tmp)) + tmp
    tmp = tmp.decode('hex')
    assert (len(tmp) == 128)
    p.send(tmp)
    #print tmp
    data = ""
    while (len(data) != 100):
        data += p.recv()
    for c in data:
        cnt[u8(c)] += 1
    p.close()
    flag = str(guessvalue(cnt)) + flag
    print i, flag
    i += 1
