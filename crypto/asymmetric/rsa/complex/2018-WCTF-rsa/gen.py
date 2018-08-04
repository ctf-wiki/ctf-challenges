from hashlib import sha256


def xor(s1, s2):
    return ''.join(chr(ord(s1[i]) ^ ord(s2[i])) for i in range(len(s1)))


encrypted_start = 0x3e09
encrypted_size = 0x14200

with open("./generator.exe", "rb") as f:
    gen = f.read()

enc = gen[encrypted_start + 32:encrypted_start + 32 + encrypted_size]

k = xor(enc[:32], gen[:32])

ps = []
for i in range(0, encrypted_size, 32):
    ps.append(xor(k, enc[i:i + 32]))
    k = sha256(k).digest()

p = "".join(ps)

# first 32 bytes of ciphertext are sha256 over plaintext
assert sha256("".join(ps)).digest() == gen[encrypted_start:encrypted_start + 32]
with open("out.exe", "wb") as f:
    f.write(p)
