#!/usr/bin/env python2
import SocketServer
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from struct import pack, unpack

from secret import AES_KEY, FLAG


class CryptoError(Exception):
    pass


def split_by(data, step):
    return [data[i : i+step] for i in xrange(0, len(data), step)]


def xor(a, b):
    assert len(a) == len(b)
    return ''.join([chr(ord(ai)^ord(bi)) for ai, bi in zip(a,b)])


def pad(msg):
    byte = 16 - len(msg) % 16
    return msg + chr(byte) * byte


def unpad(msg):
    if not msg:
        return ''
    return msg[:-ord(msg[-1])]


def tsb_encrypt(aes, msg):
    msg = pad(msg)
    iv = get_random_bytes(16)
    prev_pt = iv
    prev_ct = iv
    ct = ''
    for block in split_by(msg, 16) + [iv]:
        ct_block = xor(block, prev_pt)
        ct_block = aes.encrypt(ct_block)
        ct_block = xor(ct_block, prev_ct)
        ct += ct_block
        prev_pt = block
        prev_ct = ct_block
    return iv + ct


def tsb_decrypt(aes, msg):
    iv, msg = msg[:16], msg[16:]
    prev_pt = iv
    prev_ct = iv
    pt = ''
    for block in split_by(msg, 16):
        pt_block = xor(block, prev_ct)
        pt_block = aes.decrypt(pt_block)
        pt_block = xor(pt_block, prev_pt)
        pt += pt_block
        prev_pt = pt_block
        prev_ct = block
    pt, mac = pt[:-16], pt[-16:]
    if mac != iv:
        raise CryptoError()
    return unpad(pt)

def send_binary(s, msg):
    s.sendall(pack('<I', len(msg)))
    s.sendall(msg)

def send_enc(s, aes, msg):
    send_binary(s, tsb_encrypt(aes, msg))

def recv_exact(s, length):
    buf = ''
    while length > 0:
        data = s.recv(length)
        if data == '':
            raise EOFError()
        buf += data
        length -= len(data)
    return buf

def recv_binary(s):
    size = recv_exact(s, 4)
    size = unpack('<I', size)[0]
    return recv_exact(s, size)

def recv_enc(s, aes):
    data = recv_binary(s)
    return tsb_decrypt(aes, data)

def main(s):
    aes = AES.new(AES_KEY, AES.MODE_ECB)
    try:
        while True:
            a = recv_binary(s)
            b = recv_enc(s, aes)
            if a == b:
                if a == 'gimme_flag':
                    send_enc(s, aes, FLAG)
                else:
                    # Invalid request, send some random garbage instead of the
                    # flag :)
                    send_enc(s, aes, get_random_bytes(len(FLAG)))
            else:
                send_binary(s, 'Looks like you don\'t know the secret key? Too bad.')
    except (CryptoError, EOFError):
        pass

class TaskHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        main(self.request)

if __name__ == '__main__':
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    server = SocketServer.ThreadingTCPServer(('0.0.0.0', 1337), TaskHandler)
    server.serve_forever()
