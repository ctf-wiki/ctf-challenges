#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.log_level = "debug"

io = remote("bamboofox.cs.nctu.edu.tw", 10001)

with open("./order.txt") as f:
    payload = f.read()

io.sendlineafter(":", payload)

io.interactive()
io.close()
