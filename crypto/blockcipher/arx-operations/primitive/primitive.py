import random,sys,struct,string
from hashlib import sha256
import SocketServer
from Crypto.Util.number import getPrime
import numpy as np
from flag import FLAG

class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        print proof
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            return False
        return True

    def handle(self):
        if not self.proof_of_work():
            return
        self.request.settimeout(3)
        req = self.request
        req.sendall('Welcome to Cipher Builder\nCan you build a good cipher piece by piece?\n')
        cnt=0
        maxcnt=3
        pt='GoodCipher'
        for i in range(maxcnt):
            m=np.random.permutation(256)
            ct=''.join(map(lambda x:chr(m[ord(x)]),pt))
            req.sendall('Current ciphertext is %s\n' % ct.encode('hex'))
            cipher = []
            clen = 0
            while True:
                c=req.recv(10)
                if c.find(' ')==-1 or clen>2000:
                    break
                a,b=map(int,c.split(' ')[:2])
                if (a==0 and b>=0 and b<256) or (a==1 and b>=0 and b<8) or (a==2 and b>=0 and b<256):
                    cipher.append((a,b))
                    clen+=1
                    req.sendall('OK\n')
                else:
                    req.sendall('Error\n')
            res=''
            for ch in ct:
                tmp=ord(ch)
                for a,b in cipher:
                    if a==0:
                        tmp=(tmp+b)&0xff
                    elif a==1:
                        tmp=((tmp>>(8-b))|(tmp<<b))&0xff
                    elif a==2:
                        tmp=tmp^b
                    #print tmp,
                res+=chr(tmp)
            if res==pt:
                cnt+=1
            else:
                break
        if cnt>=maxcnt:
            req.sendall('Good job! Your flag here.\n'+FLAG+'\n')
        else:
            req.sendall("Sadely your cipher is not good\n")
        req.close()


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    print HOST
    print PORT
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
