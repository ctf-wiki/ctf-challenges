#!/usr/bin/env python

import sys
import time
import marshal
import types
import signal
import hmac 
import hashlib
import secret
try:
    from Crypto.Util import number
except ImportError:
    pass


TIMEOUT = 940
NCHALLENGES = 3
NSIZE = 1280





def send_challenges():

    code = marshal.loads("63000000000d000000070000004300000073df010000740000721d0064010064020015000000000100640200157d00006e00007401007d01007c0100640300157d02006402007d0300786f007c03006a02008300007c01006b030072a400784c007403007296007404006a05007c02008301007d04007404006a05007c02008301007d05007406007c04007c0500188301006a02008300007c0100640400146b0400724b0050714b00714b00577c04007c0500147d0300713600577c0400640500187c050064050018147d06006406007d07006407007d080078090174030072ce017404006a07007408006403007409007c01007c0700148301008302007408006403007409007c01007c070014830100640500178302008302007d09007871007c09006a02008300007c01007c0800146b0000727b016402007d0a007844007404006a0a007c0a00830100736d017404006a0700740800640300640800830200740800640300640800830200740800640300640900830200178302007d0a00712a01577c09007c0a00397d0900710b01577404006a0b007c09007c06008302006405006b0300729a0171c6006e00007404006a0c007c09007c06008302007d0b007404006a0b007c0b007c06008302006405006b030072ca0171c6006e00005071c60057640a007d0c007c03007c0b0066020053280b0000004e690700000069000000006902000000675839b4c876bedf3f6901000000674e62105839b4d03f678d976e1283c0d23f692d000000690c0000006903000000280d000000740500000046616c736574050000004e53495a45740a0000006269745f6c656e67746874040000005472756574060000006e756d626572740e0000006765745374726f6e675072696d657403000000616273740e00000067657452616e646f6d52616e67657403000000706f777403000000696e74740700000069735072696d6574030000004743447407000000696e7665727365280d00000074010000007874050000004e73697a657406000000707173697a6574010000004e740100000070740100000071740300000070686974060000006c696d69743174060000006c696d697432740100000064740300000070707074010000006574030000007a7a7a2800000000280000000073150000002f6f726967696e616c6368616c6c656e67652e7079740a0000006372656174655f6b657917000000733e000000000106010a010d0206010a010601150109010f010f04200108010e0112020601060109013c0119010601120135020e011801060112011801060105020604".decode("hex"))
    create_key = types.FunctionType(code, globals(), "create_key")
    
    ck = create_key

    challenges = []
    for _ in xrange(NCHALLENGES):
        n, e = ck()
        v = number.getRandomInteger(NSIZE-1)
        challenges.append((n, e, v))

    ctime = int(time.time())

    for c in challenges:
        n, e, v = c
        print n
        print e
        print v
    print ctime
    sys.stdout.flush()

    tohmac = repr((challenges, ctime))
    hm = hmac.new(secret.hmackey, msg=tohmac, digestmod=hashlib.sha256)
    print hm.hexdigest()
    sys.stdout.flush()


def test_challenges():
    sol = []
    for _ in xrange(NCHALLENGES):
        sol.append(int(sys.stdin.readline().strip()))

    challenges = []
    for _ in xrange(NCHALLENGES):
        n = int(sys.stdin.readline().strip())
        e = int(sys.stdin.readline().strip())
        v = int(sys.stdin.readline().strip())
        challenges.append((n, e, v))
    ctime = int(sys.stdin.readline().strip())
    givenhmac = sys.stdin.readline().strip().decode('hex')

    tohmac = repr((challenges, ctime))
    hm = hmac.new(secret.hmackey, msg=tohmac, digestmod=hashlib.sha256)
    if(not hmac.compare_digest(hm.digest(), givenhmac)):
        print "invalid hmac!"
        sys.stdout.flush()
        sys.exit(99)
    if(int(time.time()) - ctime > TIMEOUT):
        print "Too Slow!"
        sys.stdout.flush()
        sys.exit(12)

    print "Good..."
    sys.stdout.flush()

    for i in xrange(NCHALLENGES):
        n, e, v = challenges[i]
        s = sol[i]
        if pow(s, e, n) != v:
            print "Fail!"
            sys.stdout.flush()
            sys.exit(11)
            break
    else:
        print "Succcess!"
        with open("flag", "rb") as fp:
            flag = fp.read().strip()
            print flag
        sys.stdout.flush()



def main():
    print "Welcome to ASRybaB"
    sys.stdout.flush()
	
    sys.stdin.readline()

    print "1) get challenges"
    print "2) solve challenges"
    sys.stdout.flush()


    option = int(sys.stdin.readline().strip())
    if option == 1:
        send_challenges()
        sys.exit(0)
    elif option == 2:
        test_challenges()
        sys.exit(0)
    sys.exit(21)



if __name__ == "__main__":
    main()


