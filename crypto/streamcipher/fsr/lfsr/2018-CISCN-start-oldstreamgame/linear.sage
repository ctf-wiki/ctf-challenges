mask = 0b10100100000010000000100010010100

N = 32
F = GF(2)
R = [vector(F, N) for i in range(N)]
for i in range(N):
    R[i][i] = 1
print R


def lfsr(R, mask):
    lastbit = vector(F, N)
    for i in range(0, N):
        if mask >> i & 1:
            lastbit += R[i]
    output = [lastbit] + R[0:N - 1]
    return (output, lastbit)


b = ''
with open('key', 'rb') as f:
    b = f.read()
M = Matrix(F, len(b) * 8, N)

vec = vector(F, len(b) * 8)
row = 0
for i in range(len(b)):
    t = ord(b[i])
    for j in xrange(7, -1, -1):
        vec[row] = t >> j & 1
        (R, out) = lfsr(R, mask)
        M[row] = out
        row += 1
print rank(M)
print ''.join(map(str, list(M.solve_right(vec))[::-1]))
