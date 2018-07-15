#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import system
from sys import argv
import string


if __name__ == "__main__":
    flag = argv[1]
    dic = string.digits + string.ascii_letters
    last = 0
    for i in dic:
        cmd = "~/pin-3.6-gcc-linux/pin -t ./myInscount1.so -- ./ollvm {}".format((flag + i).ljust(38, '_'))
        print cmd
        system(cmd)
