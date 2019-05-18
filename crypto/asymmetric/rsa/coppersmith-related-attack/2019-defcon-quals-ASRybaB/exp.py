from __future__ import print_function

import hashlib
import hmac
import marshal
import os
import signal
import struct
import sys
import time
import types
from ast import literal_eval

import gmpy2
from Crypto.Util import number
from pwn import *

# inspired by C3CTF's POW


def pow_hash(challenge, solution):
    return hashlib.sha256(
        challenge.encode('ascii') + struct.pack('<Q', solution)
    ).hexdigest()


def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0


def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1


TIMEOUT = 940
NCHALLENGES = 3
NSIZE = 1280

possible = []
for i in range(2**12 + 1):
    ppp = pow(2, 45) + i
    if number.isPrime(ppp):
        possible.append(ppp)

print(len(possible))
context.log_level = 'debug'
p = remote('asrybab.quals2019.oooverflow.io', 1280)


def bypass_pow():
    p.recvuntil('Challenge: ')
    chall = p.recvuntil('\n', drop=True)
    p.recvuntil('n: ')
    n = p.recvuntil('\n', drop=True)
    n = int(n)
    ans = solve_pow(chall, n)
    p.sendline(str(ans))


# get d
bypass_pow()
p.sendline('')
p.recvuntil('2) solve challenges\n')
p.sendline('1')
data = []
for i in range(10):
    item = p.recvuntil('\n', drop=True)
    data.append(item)
data = map(int, data)
nlist = []
elist = []
vlist = []
for i in range(0, 9, 3):
    nlist.append(data[i])
    elist.append(data[i + 1])
    vlist.append(data[i + 2])
f = open('data.txt', 'w')
f.write(str(possible) + '\n')
f.write(str(nlist) + '\n')
f.write(str(elist) + '\n')

ctime = data[9]
mac = p.recvuntil('\n', drop=True)
f.write(str(ctime) + '\n')
f.write(str(mac) + '\n')
f.close()
print(nlist)
print(elist)
print(vlist)
print(ctime, mac)
os.system('sage boneh_durfee.sage')
dlist = open('d.txt').read().strip()
dlist = literal_eval(dlist)
p.close()

# get flag
p = remote('asrybab.quals2019.oooverflow.io', 1280)
bypass_pow()
p.sendline('')
p.recvuntil('2) solve challenges\n')
p.sendline('2')
# send sol
for i in range(len(nlist)):
    cipher = gmpy2.powmod(vlist[i], dlist[i], nlist[i])
    p.sendline(str(cipher))

for i in range(len(nlist)):
    p.sendline(str(nlist[i]))
    p.sendline(str(elist[i]))
    p.sendline(str(vlist[i]))

p.sendline(str(ctime))
p.sendline(str(mac))
p.recvuntil('Succcess!\n')
print(p.recv())
p.interactive()
