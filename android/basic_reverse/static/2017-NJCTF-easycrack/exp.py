from Crypto.Cipher import ARC4

def messageme():
    name = 'easycrack'
    init = 51
    ans = ""
    for c in name:
        init = ord(c) ^ init
        ans += chr(init)
    return ans

def decrypt(cipher,key):
    plain =""
    for i in range(0,len(cipher),len(key)):
        tmp = cipher[i:i+len(key)]
        plain +=''.join(chr(ord(tmp[i])^ord(key[i])) for i in range(len(tmp)))
    return plain

def main():
    rc4 = ARC4.new('I_am_the_key')
    cipher = 'C8E4EF0E4DCCA683088134F8635E970EEAD9E277F314869F7EF5198A2AA4'
    cipher = ''.join(chr(int(cipher[i:i+2], 16)) for i in range(0, len(cipher), 2))
    middleplain = rc4.decrypt(cipher)
    mestr = messageme()
    print decrypt(middleplain,mestr)


if __name__ == '__main__':
    main()
