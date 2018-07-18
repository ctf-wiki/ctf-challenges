import base64


def solve():
    ans = '=0HWYl1SE5UQWFfN?I+PEo.UcshU'
    length = len(ans)
    flag = [0] * length

    beg = 0
    end = length
    while beg < length / 2:
        end -= 1
        flag[beg] = chr(ord(ans[end]) + 5)
        flag[end] = ans[beg]
        beg += 1
    flag = ''.join(flag)
    print base64.b64decode(flag)
if __name__ == "__main__":
    solve()
