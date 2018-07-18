mask = 0b10100100000010000000100010010100
b = ''
N = 32
with open('key', 'rb') as f:
    b = f.read()
key = ''
for i in range(N / 8):
    t = ord(b[i])
    for j in xrange(7, -1, -1):
        key += str(t >> j & 1)
idx = 0
ans = ""
key = key[31] + key[:32]
while idx < 32:
    tmp = 0
    for i in range(32):
        if mask >> i & 1:
            tmp ^= int(key[31 - i])
    ans = str(tmp) + ans
    idx += 1
    key = key[31] + str(tmp) + key[1:31]
num = int(ans, 2)
print hex(num)
