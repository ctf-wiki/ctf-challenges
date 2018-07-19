from pwn import *
import random
import string
from hashlib import sha256

context.log_level='debug'

def dopow():
    chal = c.recvline()
    post = chal[12:28]
    tar = chal[33:-1]
    c.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c.send(found)
def dopow2():
    chal = c2.recvline()
    post = chal[12:28]
    tar = chal[33:-1]
    c2.recvuntil(':')
    found = iters.bruteforce(lambda x:sha256(x+post).hexdigest()==tar, string.ascii_letters+string.digits, 4)
    c2.send(found)

def dopad(msg):
    pad = 16 - len(msg)%16
    return msg+chr(pad)*pad

def encrypt(msg,r):
    msg=dopad(msg)
    assert len(ks)>=r*16+len(msg)
    ct=''
    for i in range(len(msg)):
        ct+=chr(ord(msg[i])^ks[r*16+i])
    return ct

def decrypt(msg,r):
    assert len(msg)%16==0
    assert len(ks)>=r*16+len(msg)
    pt=''
    for i in range(len(msg)):
        pt+=chr(ord(msg[i])^ks[r*16+i])
    return pt

HOST = '47.75.4.252'
PORT = 10003

#c = remote('127.0.0.1', 2333)
c = remote(HOST, PORT)
dopow()
n1 = '\x00'*16
c.send('\x00'+n1)
t=c.recv()
n2 = t[1:17]
mac = t[17:25]
c.send('\x01'+n2+mac)
t=c.recv(17)
assert t[1:17]==n2
t=c.recv()
plain = dopad('\x02Welcome to Sixstars Secret Storage Service\nCommands:\n\tset [key]\tstore a secret with given key\n\tget [key]\tget a secret with given key\n')
assert len(t)==len(plain)
ks = []
for i in range(len(plain)):
    ks.append(ord(t[i])^ord(plain[i]))

#c2 = remote('127.0.0.1', 2333)
c2 = remote(HOST, PORT)
dopow2()
c2.send('\x00'+n1)
t=c2.recv()
assert n2==t[1:17]
c2.send('\x01'+n2+mac)
t=c2.recv(17)
assert t[1:17]==n2
c2.recv()

c.send(encrypt('\x01'+n2+mac,1))
t=c.recv(32)
c.recv(0x90)
pt=dopad('\x02'+'invalid')
rou=1
while len(ks)<=26*16+160:
    print len(ks),rou
    c2.send(encrypt('\x02'+'aaaaa',rou))
    t2=c2.recv()
    if len(ks)<=(rou+2)*16:
        ks2=[]
        for i in range(16):
            ks2.append(ord(pt[i])^ord(t2[i]))
        ks=ks[:(rou+1)*16]
        ks.extend(ks2)
    c.send(encrypt('\x02'+'aaaaa',rou+1))
    t=c.recv()
    if len(ks)<=(rou+3)*16:
        ks2=[]
        for i in range(16):
            ks2.append(ord(pt[i])^ord(t[i]))
        ks=ks[:(rou+2)*16]
        ks.extend(ks2)
    rou += 2

c.close()
c2.close()

#c2 = remote('127.0.0.1', 2333)
c2 = remote(HOST, PORT)
dopow2()
c2.send('\x00'+n1)
t=c2.recv()
assert n2==t[1:17]
c2.send('\x01'+n2+mac)
t=c2.recv(17)
assert t[1:17]==n2
c2.recv()

c2.send(encrypt('\x02'+'get flag',1))
for i in range(12):
    t = decrypt(c2.recv(), i*2+2)
    t = t[:t.find('=?')]
    print t
    ans = safeeval.expr(t)
    c2.send(encrypt('\x02'+str(ans),i*2+3))
print decrypt(c2.recv(), 26)
    
