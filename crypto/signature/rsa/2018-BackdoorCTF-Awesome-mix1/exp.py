from Crypto.Hash import SHA
from pwn import *

from Util import PKCS1_pad

#context.log_level = 'debug'


def main():
    port = 12345
    host = "127.0.0.1"
    p = remote(host, port)
    p.recvuntil('Message   -> ')
    message = p.recvuntil('\n\nSignature -> ', drop=True)
    log.info('message: ' + message)
    signature = p.recvuntil('\n', drop=True)
    log.info('signature: ' + signature)

    h = SHA.new(message)

    m = PKCS1_pad(h.hexdigest())

    e = 1
    n = int(signature, 16) - m

    p.sendlineafter('Enter n:', str(n))
    p.sendlineafter('Enter e:', str(e))

    p.interactive()


main()
