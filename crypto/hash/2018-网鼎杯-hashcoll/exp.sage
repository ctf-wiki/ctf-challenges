from sage.all import *

mod = 2**256
h0 = 45740974929179720441799381904411404011270459520712533273451053262137196814399

g = 2**168 + 355


def shitty_hash(msg):
    h = h0
    msg = map(ord, msg)
    for i in msg:
        h = (h + i) * g
        # This line is just to screw you up :))
        h = h & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    return h - 0xe6168647f636


K = 2**200
N = 50
base_str = 'a' * N
base = map(ord, base_str)
m = Matrix(ZZ, N + 1, N + 2)
for i in xrange(N + 1):
    ge = ZZ(pow(g, N - i, mod))
    m[i, i] = 1
    m[i, N + 1] = ZZ(ge * K)
m[i, N + 1] = ZZ(K * mod)

ml = m.LLL()
ttt = ml.rows()[0]
print "result:", ttt
if ttt[-1] != 0:
    print "Zero not reached, increase K"
    exit()
else:
    msg = []
    for i in xrange(N):
        msg.append(base[i] + ttt[i])
        if not (0 <= msg[i] <= 255):
            print "Need more bytes!"
            quit()
    print msg
    other = ''.join(map(chr, msg))

    print shitty_hash(base_str)
    print shitty_hash(other)
