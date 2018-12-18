from random import randint
import json


class Pykemon(object):
    pykemon = [
            [100, 'Pydiot', 'Pydiot','images/pydiot.png', 'Pydiot is an avian Pykamon with large wings, sharp talons, and a short, hooked beak'], 
            [90, 'Pytata', 'Pytata', 'images/pytata.png', 'Pytata is cautious in the extreme. Even while it is asleep, it constantly listens by moving its ears around.'],
            [80, 'Pyliwag', 'Pyliwag', 'images/pyliwag.png', 'Pyliwag resembles a blue, spherical tadpole. It has large eyes and pink lips.'],
            [70, 'Pyrasect', 'Pyrasect', 'images/pyrasect.png','Pyrasect is known to infest large trees en masse and drain nutrients from the lower trunk and roots.'],
            [60, 'Pyduck', 'Pyduck', 'images/pyduck.png','Pyduck is a yellow Pykamon that resembles a duck or bipedal platypus'],
            [50, 'Pygglipuff', 'Pygglipuff', 'images/pygglipuff.png','When this Pykamon sings, it never pauses to breathe.'],
            [40, 'Pykachu', 'Pykachu', 'images/pykachu.png','This Pykamon has electricity-storing pouches on its cheeks. These appear to become electrically charged during the night while Pykachu sleeps.'],
            [30, 'Pyrigon', 'Pyrigon', 'images/pyrigon.png','Pyrigon is capable of reverting itself entirely back to program data and entering cyberspace.'],
            [20, 'Pyrodactyl', 'Pyrodactyl', 'images/pyrodactyl.png','Pyrodactyl is a Pykamon from the age of dinosaurs'],
            [10, 'Pytwo', 'Pytwo', 'images/pytwo.png','Pytwo is a Pykamon created by genetic manipulation'],
            [0, 'FLAG', 'FLAG','images/flag.png', 'PCTF{XXXXX}']
            ]


    def __init__(self, name=None, hp=None):
        pykemon = Pykemon.pykemon
        if not name:              
            i = randint(0,10)
        else:
            count = 0
            for p in pykemon:
                if name in p:
                    i = count
                count += 1
        
        self.name = pykemon[i][1]
        self.nickname = pykemon[i][2]
        self.sprite = pykemon[i][3]
        self.description = pykemon[i][4]
        self.hp = hp
        if not hp:
            self.hp = randint(1,100)
        self.rarity = pykemon[i][0]
        self.pid = self.name + str(self.hp)
        

class Room(object):
    def __init__(self):
        self.rid = 0
        self.pykemon_count = randint(5,15)
        self.pykemon = []
        
        if not self.pykemon_count:
            return 
        while len(self.pykemon) < self.pykemon_count:
            p = Pykemon()
            self.pykemon.append(p.__dict__)
        return 

class Map(object):
    def __init__(self):
        self.size = 10


