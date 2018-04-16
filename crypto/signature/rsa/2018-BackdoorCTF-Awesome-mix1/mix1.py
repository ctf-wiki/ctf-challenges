#!/usr/bin/python -u

import sys

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as RSAsign

from SECRET import flag
from Util import PKCS1_pad as pad


def verify(s, m, n, e):
    if pow(s, e, n) == pad(m):
        return True
    else:
        return False


key = RSA.generate(1024)

message = "super important information for admin only"

h = SHA.new(message)
signer = RSAsign.new(key)

signature = signer.sign(h)
s = int(signature.encode("hex"), 16)

print "Welcome to admin's music portal.\nTo verify that you are the owner of this service\nsend the public key which will verify the following signature :\n"

print "Message   ->", message
print
print "Signature ->", signature.encode("hex")
print

sys.stdout.flush()

n = long(raw_input("Enter n:"))
e = long(raw_input("Enter e:"))
sys.stdout.flush()
input_key = RSA.construct((n, e))

if verify(s, h.hexdigest(), n, e):
    print flag
else:
    print "Music is only for admin's eyes."

sys.stdout.flush()
