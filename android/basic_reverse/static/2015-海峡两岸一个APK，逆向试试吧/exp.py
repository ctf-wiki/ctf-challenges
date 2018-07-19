s = "QflMn`fH,ZHVW^7c"
flag = ""
for idx,c in enumerate(s):
    tmp = ord(c)
    if idx<8:
        tmp-=3
    flag +=chr(tmp+idx)
print flag
