#!/usr/bin/env python2

from flag import FLAG

h0 = 45740974929179720441799381904411404011270459520712533273451053262137196814399

# 2**168 + 355
g = 374144419156711147060143317175368453031918731002211L


def shitty_hash(msg):
    h = h0
    msg = map(ord, msg)
    for i in msg:
        h = (h + i) * g
        # This line is just to screw you up :))
        h = h & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    return h - 0xe6168647f636


if __name__ == '__main__':
    try:
        introduction = """
        .--.     .------------------------.
        | __\    |                        |
        | > <   <  Homies, Hash collision |
        |  \|    |                        |
        |/_//    `------------------------'
        |  /
        `-'
        I never want to create challenges that people can grab random scripts to solve it. Nah
        """

        print introduction

        m1 = raw_input('m1 : ')
        m2 = raw_input('m2 : ')

        assert m1 != m2

        #print "m1 = {!r}".format(m1)
        #print "m2 = {!r}".format(m2)

        hash1 = shitty_hash(m1)
        hash2 = shitty_hash(m2)

        if hash1 == hash2:
            print "\nThe flag is simple, it is 'the flag' :)) "
            print FLAG
        else:
            print 'Wrong.'

    except:
        print "Take your time to think of the inputs."
        pass
