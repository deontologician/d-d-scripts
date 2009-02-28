
from random import randint

def d20():
    return randint(1,20)

def mml(mon_type, num, init_mod):
    mon_list = []
    for i in xrange(num):
        mon = Player(mon_type + " " + chr(ord('A')+i), init_mod)
        mon_list.append(mon)
    return mon_list


class Player(object):
    def __init__(self, name, init_mod):
        self.name = name
        self.init_mod = init_mod

    def __repr__(self):
        return self.name


class Encounter(object):
    def __init__(self, players, monsters, player_mod = 0, monster_mod = 0):
        self.players = players
        self.monsters = monsters
        self.player_mod = player_mod
        self.monster_mod = monster_mod
        self.init_list = []
        for plyr in self.players:
            self.init_list.append((d20() + plyr.init_mod + self.player_mod,
                                   plyr.name ))
        for mnstr in self.monsters:
            self.init_list.append((d20() + mnstr.init_mod + self.monster_mod,
                                   mnstr.name))
        
        self.init_list.sort(cmp=(lambda (x,i),(y,j): y-x))

    def __repr__(self):
        ret_string = ""
        for (num,name) in self.init_list:
            ret_string += str(num) + " -> " + name + "\n"
        return ret_string


plist = [Player("Rivu", 6),
         Player("Ash",3),
         Player("Frommer",4),
         Player("Donn",2),
         Player("Kelvin",3)]

mlist = mml("Demon",4,3) + mml("Sharpshooter",2,4)
