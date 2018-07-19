from pwn import *
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


#c = remote('127.0.0.1', 2333)
c = remote('47.75.4.252', 10002)
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
c.send(encrypt('\x02'+'get flag',1))
cflag=c.recv()
c.send(encrypt('\x02'+'set a',3))
t=decrypt(c.recv(),4)
print t
c.send(encrypt('\x02'+'\x00'*62,5)+'\x00'*512)
t=decrypt(c.recv(),6)
print t
pt='\x02'+'\x00'*62+'\x01'
rou=7
while len(ks)<=2*16+len(cflag):
    c.send(encrypt('\x02'+'get a',rou))
    t=c.recv()
    if len(ks)<=(rou+1)*16+len(pt):
        ks2=[]
        for i in range(len(pt)):
            ks2.append(ord(pt[i])^ord(t[i]))
        ks=ks[:(rou+1)*16]
        ks.extend(ks2)
    rou += 2
print decrypt(cflag,2)
