from Crypto.Util.number import long_to_bytes,bytes_to_long



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
import subprocess
import random
def get_iv(io):
    rsa_c, aes_c=encrypt_io(io,"1")
    return bytes_to_long(aes_c[0:16])
def splitInto32(w128):
    w1 = w128 & (2**32-1)
    w2 = (w128 >> 32) & (2**32-1)
    w3 = (w128 >> 64) & (2**32-1)
    w4 = (w128 >> 96)
    return w1,w2,w3,w4
def sign(iv):
    # converts a 32 bit uint to a 32 bit signed int
    if(iv&0x80000000):
        iv = -0x100000000 + iv
    return iv
def get_state(io):
    numbers=[]
    for i in range(156):
        print i
        numbers.append(get_iv(io))
    observedNums = [sign(w) for n in numbers for w in splitInto32(n)]
    o = subprocess.check_output(["java", "Main"] + map(str, observedNums))
    stateList = [int(s) % (2 ** 32) for s in o.split()]
    r = random.Random()
    state = (3, tuple(stateList + [624]), None)
    r.setstate(state)
    return r.getrandbits(128)
