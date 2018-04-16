def PKCS1_pad(data):
    asn1 = "3021300906052b0e03021a05000414"
    ans = asn1 + data
    n = len(ans)
    return int(('00' + '01' + 'ff' * (1024 / 8 - n / 2 - 3) + '00' + ans), 16)
