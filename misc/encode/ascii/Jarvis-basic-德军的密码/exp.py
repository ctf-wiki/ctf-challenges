cipher = '000000000000000000000000000000000000000000000000000101110000110001000000101000000001'
result = []
key = "WELCOMETOCFF"
for i in range(0, len(cipher), 7):
    result.append(int('0' + cipher[i:i + 7], 2))
flag = ""
for index, value in enumerate(key):
    flag += chr(ord(value) ^ result[index])
print flag
