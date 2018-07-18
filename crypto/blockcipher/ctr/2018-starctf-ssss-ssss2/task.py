import random,sys,string
from hashlib import sha256
import SocketServer
from Crypto.Util import Counter 
from Crypto.Cipher import AES
import binascii
import os
import numpy as np
import hmac,hashlib
import argon2
from flag import FLAG

secret='******' # REDACTED HERE
assert len(secret)==6

menu = 'Welcome to Sixstars Secret Storage Service\nCommands:\n\tset [key]\tstore a secret with given key\n\tget [key]\tget a secret with given key\n'

class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(4)
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            return False
        return True

    def dosend(self, msg):
        if self.k!='':
            self.r += 1
            ctr_e=Counter.new(128, initial_value=self.r)
            a=AES.new(key=self.k,mode=AES.MODE_CTR,counter=ctr_e)
            pad = 16 - len(msg)%16
            plain = msg + chr(pad)*pad
            msg = ''
            for i in range(len(plain)/16):
                msg += a.encrypt(plain[i*16:(i+1)*16])
        self.request.sendall(msg)

    def dorecv(self):
        msg = self.request.recv(1024)
        assert len(msg)>0
        if self.k!='':
            self.r += 1
            ctr_e=Counter.new(128, initial_value=self.r)
            a=AES.new(key=self.k,mode=AES.MODE_CTR,counter=ctr_e)
            cmsg = msg
            msg = ''
            assert len(cmsg)%16==0
            for i in range(len(cmsg)/16):
                msg += a.decrypt(cmsg[i*16:(i+1)*16])
            msg = msg[:-ord(msg[-1])]
        return msg

    def handle(self):
        if not self.proof_of_work():
            return
        self.n1 = ''
        self.n2 = ''
        self.buf = ''
        self.mk = ''
        self.k = ''
        self.r = 0
        self.dat = {}
        self.dat['flag'] = os.urandom(140) + FLAG
        while True:
            p=self.dorecv()
            if p[0]=='\x00':
                if len(p)<17:
                    self.dosend('\xff'+'\x01')
                    break
                self.n1 = p[1:17]
                self.n2 = hashlib.sha512(self.n1).digest()[:16]
                self.buf = argon2.argon2_hash(password=secret, salt=self.n1+self.n2, t=100, m=1000, p=10, buflen=128, argon_type=argon2.Argon2Type.Argon2_i)
                self.mk = self.buf[:16]
                msg = self.n2
                mac = hmac.new(self.mk,msg,hashlib.sha512).digest()[:8]
                self.dosend('\x00'+msg+mac)
            elif p[0]=='\x01':
                if len(p)<25:
                    self.dosend('\xff'+'\x01')
                    break
                self.r = int(binascii.hexlify(p[1:17]),16)
                mac = hmac.new(self.mk,p[1:17],hashlib.sha512).digest()[:8]
                if mac != p[17:25]:
                    self.dosend('\xff'+'\x02')
                    break
                msg = '\x01' + p[1:17]
                self.dosend(msg)
                self.k = self.buf[16:32]
                msg = '\x02' + menu
                self.dosend(msg)
            elif p[0]=='\x02':
                if self.k == '':
                    self.dosend('\xff'+'\x03')
                    break
                k=p[5:]
                if p[1:5] == 'set ':
                    self.dosend('\x02'+'value?')
                    v = self.dorecv()
                    assert v[0] == '\x02'
                    v = v[1:]
                    self.dat[k] = v
                    self.dosend('\x02'+'OK')
                elif p[1:5] == 'get ':
                    v = self.dat[k]
                    self.dosend('\x02'+v)
                else:
                    self.dosend('\x02'+'invalid')
            else: 
                self.dosend('\xff'+'\x05')
                break
        self.request.close()


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10002
    print HOST
    print PORT
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
