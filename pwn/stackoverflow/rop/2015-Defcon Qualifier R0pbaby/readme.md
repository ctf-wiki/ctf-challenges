# 思路

## 确定保护

```text
Arch:     amd64-64-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
FORTIFY:  Enabled
```

开启了堆栈执行保护。

## 确定漏洞

在选项3对应的代码中

```C
      ReadStr(nptr, 1024LL);
      v4 = (signed int)strtol(nptr, 0LL, 10);
      if ( v4 - 1 > 1023 )
      {
        puts("Invalid amount.");
      }
      else
      {
        if ( v4 )
        {
          v5 = 0;
          v6 = 0LL;
          while ( 1 )
          {
            v7 = _IO_getc(stdin);
            if ( v7 == -1 )
              break;
            nptr[v6] = v7;
            v6 = ++v5;
            if ( v4 <= v5 )
              goto LABEL_22;
          }
          v6 = v5 + 1;
        }
        else
        {
          v6 = 0LL;
        }
LABEL_22:
        memcpy(&savedregs, nptr, v6);
```

可以看到在memcpy处存在栈溢出，我们可以使用nptr来覆盖栈保存的rbp以及返回地址等内容。所以我们可以使用rop来快速实现漏洞利用

## 确定地址

- system
  - 可以直接根据选项2直接得到system的地址
- libc基地址
  - 进而根据libc数据库找到相应的libc此后便可以找到libc基地址
- /bin/sh
  - 同时也可以找到/bin/sh地址

## 寻找gadgets

由于该程序是64位程序，所以我们需要将/bin/sh的地址放到rdi寄存器中。所以我们需要找到可以操作rdi的gadgets。直接使用源程序并不可行，因为源程序有PIE保护，并且我们不知道每次源程序加载的位置在哪里。但是我们知道libc中的地址，所以可以去libc中寻找。

## 构造payload

最后构造的payload如下

```text
[fake rbp][rdi_ret][binsh_addr][system_addr]
```

# exp

参见exp.py。