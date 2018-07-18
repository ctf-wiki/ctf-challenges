from sage.all import *

mask = 0b10100100000010000000100010010100

N = 32
F = GF(2)

b = ''
with open('key', 'rb') as f:
    b = f.read()

R = [vector(F, N) for i in range(N)]
for i in range(N):
    R[i][N - 1] = mask >> (31 - i) & 1
for i in range(N - 1):
    R[i + 1][i] = 1
M = Matrix(F, R)
M = M ^ N

vec = vector(F, N)
row = 0
for i in range(N / 8):
    t = ord(b[i])
    for j in xrange(7, -1, -1):
        vec[row] = t >> j & 1
        row += 1
print rank(M)
num = int(''.join(map(str, list(M.solve_left(vec)))), 2)
print hex(num)
