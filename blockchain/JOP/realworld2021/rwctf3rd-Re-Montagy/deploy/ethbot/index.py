import sys
import os
from conf.base import alarmsecs, workdir
import signal
import codecs
from src.main import main
import hashlib
import random
import string

def getflag(seed, teamtoken):
    token=teamtoken
    real_flag=hashlib.md5((seed+'&'+hashlib.sha1(token[::-1].encode()).hexdigest()[:10]).encode()).hexdigest()
    return 'flag{' + real_flag + '}'

def generatepow(difficulty):
    prefix = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
    msg="sha256("+prefix+" + ?).binary.endswith('"+"0"*difficulty+"')"
    return prefix,msg

def pow(prefix,difficulty,answer):
    hashresult=hashlib.sha256((prefix+answer).encode()).digest()
    bits=bin(int(hashlib.sha256((prefix+answer).encode()).hexdigest(),16))[2:]
    if bits.endswith("0"*difficulty):
        return True
    else:
        return False


print("[$] Welcome to Re:Montagy.")
prefix,msg=generatepow(5)
print("[+]",msg)
answer=input("[-] ?=")

if not pow(prefix,5,answer):
    print("[+]wrong proof")
    sys.exit(0)
print("[+] passed")



class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.path.append(workdir)
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdout = Unbuffered(sys.stdout)
signal.alarm(alarmsecs)
os.chdir(workdir)
main()