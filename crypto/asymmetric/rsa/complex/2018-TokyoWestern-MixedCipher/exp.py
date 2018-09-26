from zio import *
import primefac
from Crypto.Util.number import long_to_bytes,bytes_to_long
target=("crypto.chal.ctf.westerns.tokyo",5643)
e=65537

def get_enc_key(io):
    io.read_until("4: get encrypted keyn")
    io.writeline("4")
    io.read_until("here is encrypted key :)n")
    c=int(io.readline()[:-1],16)
    return c

def encrypt_io(io,p):
    io.read_until("4: get encrypted keyn")
    io.writeline("1")
    io.read_until("input plain text: ")
    io.writeline(p)
    io.read_until("RSA: ")
    rsa_c=int(io.readline()[:-1],16)
    io.read_until("AES: ")
    aes_c=io.readline()[:-1].decode("hex")
    return rsa_c,aes_c

def decrypt_io(io,c):
    io.read_until("4: get encrypted keyn")
    io.writeline("2")
    io.read_until("input hexencoded cipher text: ")
    io.writeline(long_to_bytes(c).encode("hex"))
    io.read_until("RSA: ")
    return io.read_line()[:-1].decode("hex")

def get_n(io):
    rsa_c,aes_c=encrypt_io(io,long_to_bytes(2))
    n=pow(2,65537)-rsa_c
    for i in range(3,6):
        rsa_c, aes_c = encrypt_io(io, long_to_bytes(i))
        n=primefac.gcd(n,pow(i,65537)-rsa_c)
    return n

def check_n(io,n):
    rsa_c, aes_c = encrypt_io(io, "123")
    if pow(bytes_to_long("123"), e, n)==rsa_c:
        return True
    else:
        return False


import gmpy2
def guess_m(io,n,c):
    k=1
    lb=0
    ub=n
    while ub!=lb:
        print lb,ub
        tmp = c * gmpy2.powmod(2, k*e, n) % n
        if ord(decrypt_io(io,tmp)[-1])%2==1:
            lb = (lb + ub) / 2
        else:
            ub = (lb + ub) / 2
        k+=1
    print ub,len(long_to_bytes(ub))
    return ub


io = zio(target, timeout=10000, print_read=COLORED(NONE, 'red'),print_write=COLORED(NONE, 'green'))
n=get_n(io)
print check_n(io,n)
c=get_enc_key(io)
print len(decrypt_io(io,c))==16


m=guess_m(io,n,c)
for i in range(m - 50000,m+50000):
    if pow(i,e,n)==c:
        aeskey=i
        print long_to_bytes(aeskey)[-1]==decrypt_io(io,c)[-1]
        print "found aes key",hex(aeskey)

import fuck_r
next_iv=fuck_r.get_state(io)
print "##########################################"
print next_iv
print aeskey
io.interact()
