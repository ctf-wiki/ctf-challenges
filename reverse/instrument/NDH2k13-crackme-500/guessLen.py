#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from sys import argv
import string

pinPath = "/home/m4x/pin-3.6-gcc-linux/pin"
pinInit = lambda tool, elf: Popen([pinPath, '-t', tool, '--', elf], stdin = PIPE, stdout = PIPE)
pinWrite = lambda cont: pin.stdin.write(cont)
pinRead = lambda : pin.communicate()[0]

if __name__ == "__main__":
    last = 0
    for i in xrange(1, 30):
        pin = pinInit("./myInscount0.so", "./crackme")
        pinWrite("a" * i + '\n')
        now = int(pinRead().split("Count: ")[1])
        
        print "inputLen({:2d}) -> ins({}) -> delta({})".format(i, now, now - last)
        last = now
