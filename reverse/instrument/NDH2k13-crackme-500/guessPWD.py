#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from sys import argv
import string
import pdb

pinPath = "/home/m4x/pin-3.6-gcc-linux/pin"
pinInit = lambda tool, elf: Popen([pinPath, '-t', tool, '--', elf], stdin = PIPE, stdout = PIPE)
pinWrite = lambda cont: pin.stdin.write(cont)
pinRead = lambda : pin.communicate()[0]

if __name__ == "__main__":
    last = 0
    #  dic = map(chr, xrange(0x20, 0x80))
    dic = string.ascii_letters + string.digits + "+_ "
    pwd = '?' * 8
    dicIdx = 0
    pwdIdx = 0

    while True:
        pwd = pwd[: pwdIdx] + dic[dicIdx] + pwd[pwdIdx + 1: ]
        #  pdb.set_trace()
        pin = pinInit("./myInscount1.so", "./crackme")
        pinWrite(pwd + '\n')
        now = int(pinRead().split("Count: ")[1])

        print "input({}) -> now({}) -> delta({})".format(pwd, now, now - last)

        if now - last > 2000 and dicIdx:
            pwdIdx += 1
            dicIdx = -1
            last = 0
            if pwdIdx >= len(pwd):
                print "Found pwd: {}".format(pwd)
                break

        dicIdx += 1
        last = now
