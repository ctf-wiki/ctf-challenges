#from flag import flag
#assert flag.startswith("flag{")
#assert flag.endswith("}")
#assert len(flag)==25


def lfsr(R, mask):
    output = (R << 1) & 0xffffff
    i = (R & mask) & 0xffffff
    lastbit = 0
    while i != 0:
        lastbit ^= (i & 1)
        i = i >> 1
    output ^= lastbit
    return (output, lastbit)


def compare(flag, key):
    ans = ""
    mask = 0b1010011000100011100
    for i in range(12):
        tmp = 0
        for j in range(8):
            (flag, out) = lfsr(flag, mask)
            tmp = (tmp << 1) ^ out
        if chr(tmp) != key[i]:
            return False
    return True


def solve():
    num = pow(2, 25 - 5 - 1)
    f = open("key")
    key = f.read()
    print len(key)
    f.close()
    for i in range(num):
        if compare(i, key):
            print bin(i)
            break


solve()
