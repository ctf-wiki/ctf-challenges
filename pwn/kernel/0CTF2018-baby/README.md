# 2018 0CTF Finals Baby Kernel

漏洞类型： `Double Fetch`

flag： `flag{THIS_WILL_BE_YOUR_FLAG_1234}`

## Writeup

根据 `Double Fetch` 漏洞原理，发现此题目存在一个 `Double Fetch` 漏洞，当用户输入数据通过验证后，再将 `flag_str` 所指向的地址改为 flag 硬编码地址后，即会输出 flag 内容。

首先，利用提供的 `cmd=0x6666` 功能，获取内核中 flag 的加载地址。

> 内核中以 `printk` 输出的内容，可以通过 `dmesg` 命令查看。

然后，构造符合 `cmd=0x1337` 功能的数据结构，其中 `flag_len` 可以从硬编码中直接获取为 33， `flag_str` 指向一个用户空间地址。

最后，创建一个恶意线程，不断的将 `flag_str` 所指向的用户态地址修改为 flag 的内核地址以制造竞争条件，从而使其通过驱动中的逐字节比较检查，输出 flag 内容。

```bash
└─[$] <git:(master*)> ./start.sh 

Boot took 0.52 seconds

/ $ ./exp
[+]flag addr: 0xffffffffc006b028
[+]result is :
[    3.599210] Your flag is at ffffffffc006b028! But I don't think you know it's content
[    3.689193] Looks like the flag is not a secret anymore. So here is it flag{THIS_WILL_BE_YOUR_FLAG_1234}
```

> `exp.c` 中碰撞次数为0x1000，若不成功，可尝试将 `TRYTIME` 增大，或多试几次。