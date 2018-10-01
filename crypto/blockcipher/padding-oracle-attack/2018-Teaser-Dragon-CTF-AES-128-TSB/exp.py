from pwn import *
#context.log_level = 'debug'
#p = remote('aes-128-tsb.hackable.software', 1337)

p = remote('127.0.0.1', 1337)


def pad(msg):
    byte = 16 - len(msg) % 16
    return msg + chr(byte) * byte


def send_data(data=''):
    size = len(data)
    p.send(p32(size))
    if size:
        p.send(data)


def recv_data():
    length = u32(p.recvn(4, timeout=3))
    data = p.recvn(length, timeout=3)
    return length, data


def split_by(data, step):
    return [data[i:i + step] for i in xrange(0, len(data), step)]


def xor(a, b):
    assert len(a) == len(b)
    return ''.join([chr(ord(ai) ^ ord(bi)) for ai, bi in zip(a, b)])


"""
every item is a pair [a,b]
a is the xor list
b is the idx which is zero when xored
"""
xor_byte_map = []
for i in range(256):
    a = []
    b = 0
    for j in range(256):
        tmp = i ^ j
        if tmp > 0 and tmp <= 15:
            a.append(1)
        else:
            a.append(0)
        if tmp == 0:
            b = j
    xor_byte_map.append([a, b])


def getlast_byte(iv, block):
    iv_pre = iv[:15]
    iv_last = ord(iv[-1])
    tmp = []
    print('get last byte')
    for i in range(256):
        send_data('')
        iv = iv_pre + chr(i)
        tmpblock = block[:15] + chr(i ^ ord(block[-1]) ^ iv_last)
        payload = iv + tmpblock + iv
        send_data(payload)
        length, data = recv_data()
        if 'Looks' in data:
            tmp.append(1)
        else:
            tmp.append(0)
    last_bytes = []
    for i in range(256):
        if tmp == xor_byte_map[i][0]:
            last_bytes.append(xor_byte_map[i][1])
    print('possible last byte is ' + str(last_bytes))
    return last_bytes


def dec_block(iv, block):
    iv_pre = iv[:15]
    iv_last = ord(iv[-1])
    last_bytes = getlast_byte(iv, block)

    print('try to get plain')
    plain0 = ''
    for last_byte in last_bytes:
        plain0 = ''
        for i in range(15):
            print 'idx:', i
            tag = False
            for j in range(256):
                send_data(plain0 + chr(j))
                pad_size = 15 - i
                iv = iv_pre + chr(pad_size ^ last_byte)
                tmpblock = block[:15] + chr(
                    pad_size ^ last_byte ^ ord(block[-1]) ^ iv_last
                )
                payload = iv + tmpblock + iv
                send_data(payload)
                length, data = recv_data()
                if 'Looks' not in data:
                    # success
                    plain0 += chr(j)
                    tag = True
                    break
            if not tag:
                break
        # means the last byte is ok
        if plain0 != '':
            break
    plain0 += chr(iv_last ^ last_byte)
    return plain0


def main():
    print('try to get the plain of zero cipher')
    plain0 = dec_block('1' * 16, '1' * 16)
    plain0 = xor(plain0, '1' * 16)
    cipher0 = chr(0) * 16
    print("zero cipher\'s plain is " + plain0.encode('hex'))

    print('get the cipher of flag')
    gemmi_iv1 = xor(pad('gimme_flag'), plain0)
    gemmi_c1 = xor(gemmi_iv1, cipher0)
    payload = gemmi_iv1 + gemmi_c1 + gemmi_iv1
    send_data('gimme_flag')
    send_data(payload)
    flag_len, flag_cipher = recv_data()
    print('the flag cipher is ' + flag_cipher.encode('hex'))
    flag_cipher = split_by(flag_cipher, 16)

    print('decrypt the blocks one by one')
    plain = ''
    for i in range(len(flag_cipher) - 1):
        print('block: ' + str(i))
        if i == 0:
            plain += dec_block(flag_cipher[i], flag_cipher[i + 1])
        else:
            iv = plain[-16:]
            cipher = xor(xor(iv, flag_cipher[i + 1]), flag_cipher[i])
            plain += dec_block(iv, cipher)
            pass
        print('now plain: ' + plain)
    print plain
    p.close()


if __name__ == "__main__":
    main()
