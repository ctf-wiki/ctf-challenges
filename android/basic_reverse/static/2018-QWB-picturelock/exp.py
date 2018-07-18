#!/usr/bin/env python

import itertools

sig = 'f8c49056e4ccf9a11e090eaf471f418d'

from Crypto.Cipher import AES

def decode_sig(payload):
    ans = ""
    for i in range(len(payload)):
        ans +=chr(ord(payload[i]) ^ ord(sig[(16+i)%32]))
    return ans

def dec_aes():
	data = open('flag.jpg.lock', 'rb').read()
	jpg_data = ''
	f = open('flag.jpg', 'wb')
	idx = 0
	i = 0
	cipher1 = AES.new(sig[:0x10])
	cipher2 = AES.new(sig[0x10:])
	while idx < len(data):
		read_len = ord(sig[i % 32])
		payload = data[idx:idx+read_len]
		#print('[+] Read %d bytes' % read_len)
		print('[+] Totally %d / %d bytes, sig index : %d' % (idx, len(data), i))

		if read_len % 2 == 0:
			f.write(cipher1.decrypt(payload[:0x10]))
		else:
			f.write(cipher2.decrypt(payload[:0x10]))
		f.write(decode_sig(payload[16:]))
		f.flush()
		idx += read_len
		i += 1
	print('[+] Decoding done ...')
	f.close()

dec_aes()
