import hashlib

addStr = 'TSw8BK8m'
knownMd5 = '83bdef'

dict = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def md5(text):
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()

for i in dict:
  for j in dict:
      for k in dict:
          for l in dict:
            x = i + k + j + l
            codeMd5 = md5(x+addStr)
            if codeMd5[:6] == knownMd5:
                print x, x+addStr
