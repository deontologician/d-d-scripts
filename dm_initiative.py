from dm_common import *

def mml(mon_type, num, init_mod):
    "Quickly creates a list of monsters of the given quantity"
    mon_list = []
    for i in xrange(num):
        mon = Player(mon_type + " " + chr(ord('A')+i), init_mod)
        mon_list.append(mon)
    return mon_list



class Encounter(object):
    "Simulates an encounter given a player and monster list"

    def __init__(self, players, monsters, player_mod = 0, monster_mod = 0):
        self.players = players
        self.monsters = monsters
        self.player_mod = player_mod
        self.monster_mod = monster_mod
        self.init_list = []
        self.roll_initiative()

    def roll_initiative(self):
        "Rolls the initiative and creates the initiative order"
        self.init_list += [(d20() + plyr.init_mod + self.player_mod,
                            plyr.name) for plyr in self.players]

        self.init_list += [(d20() + mnstr.init_mod + self.monster_mod,
                            mnstr.name) for mnstr in self.monsters]
        
        self.init_list.sort(cmp=(lambda (x,i),(y,j): y-x))

    def __repr__(self):
        ret_string = ""
        for (num,name) in self.init_list:
            ret_string += str(num) + " -> " + name + "\n"
        return ret_string
