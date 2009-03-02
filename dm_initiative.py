from dm_common import d20
from dm_common import Player
from dm_common import Monster
from dm_common import Commandline
from dm_common import ordinal

from time import strftime
from random import choice

class Session(object):
    "A series of encounters "
    def __init__(self):
        self.name = raw_input("Name of Session: ").strip()
        self.date = strftime("%A %B %d, %Y %I:%M %p")
        self.encounters = []
        self.plist = []
        self.new_players()
        self.next_encounter()

    def next_encounter(self):
        "Adds a new encounter to the list"
        self.encounters.append(new_encounter(self.plist))

    def __repr__(self):
        rep = self.name + "\n" + self.date + "\n"
        for i,enco in enumerate(self.encounters):
            rep += "Encounter #%d\n" % (i+1)
            rep += str(enco)
        return rep 

    def curr_enc(self):
        return self.encounters[-1]

    def new_players(self):
        "Makes a new list of characters"
        num_players = int(raw_input("How many players are there? "))
        self.plist = []
        for i in xrange(num_players):
            name = raw_input("%s player's name: " % ordinal(i+1))
            init = int(raw_input("%s's initiative modifier: " % name))
            self.plist.append(Player(name, init))

    def save(self):
        default_name = self.name.title().replace(" ","") + ".txt"
        filename = raw_input("Filename (default '%s'): "\
                                 % default_name).strip()
        if filename == "":
            filename = default_name
        f = open(filename,'w')
        f.write(str(self))
        print "Encounter saved to %s " % filename

    def print_current_enc(self):
        print self.encounters[-1]
    

class Encounter(object):
    "Simulates an encounter given a player and monster list"

    def __init__(self, enc_name, plist, player_mod = 0, monster_mod = 0):
        self.enc_name = enc_name
        self.p_mod = player_mod
        self.m_mod = monster_mod
        self.init_list = []
        self.plist = plist
        self.mlist = []
        self.new_monsters()
        self.roll_initiative()

    def roll_initiative(self):
        "Rolls the initiative and creates the initiative order"
        self.init_list += [(d20() + plyr.init_mod + self.p_mod,
                            plyr) for plyr in self.plist]

        self.init_list += [(d20() + mnstr.init_mod + self.m_mod,
                            mnstr) for mnstr in self.mlist]

        self.init_list.sort(cmp=init_comparer)

    def __repr__(self):
        ret_string = ("-[%s]-" % self.enc_name).center(80) + "\n"
        for (num,name) in self.init_list:
            ret_string += str(num) + " -> " + str(name) + "\n"
        return ret_string + "\n"

    def new_monsters(self):
        "Creates new monsters from the command line"
        self.mlist = []
        def mml(mon_type, num, init_mod, hp):
            for pl in xrange(num):
                mon = Monster(mon_type + " " + chr(ord('A')+pl),
                              init_mod, hp)
                self.mlist.append(mon)

        while True:
            mon_name = raw_input("Monster name: ").title()
            mon_num = int(raw_input("Number of %s(s): " % mon_name))
            mon_init = int(raw_input("%s initiative: " % mon_name))
            mon_hp = int(raw_input("%s hp: " % mon_name))
            mml(mon_name, mon_num, mon_init, mon_hp)
            more = raw_input("More monster types? (yes/no)").strip().lower()
            if more == "no":
                print self.mlist
                break


def init_comparer(tupleA, tupleB):
    "Compares two (init, Player) tuples for precedence"
    total_initA, A = tupleA
    total_initB, B = tupleB
    if total_initA > total_initB:
        return -1
    elif total_initA < total_initB:
        return 1
    else: # absolute inits are the same, get the highest mod
        if A.init_mod > B.init_mod:
            return -1
        elif A.init_mod < B.init_mod:
            return 1
        else: # flip a coin if all else fails
            return choice([-1,1])
      
def new_encounter(plist):
    enc_name = raw_input("Encounter name: ")
    p_init = int(raw_input("Enter situational init modifier"\
                               " for the players:"))
    m_init = int(raw_input("Enter situational init modifier"\
                               " for the monsters:"))
    enco = Encounter(enc_name, plist, player_mod = p_init, 
                     monster_mod = m_init)
    print "Ok, here is the encounter initiative order:"
    print enco
    return enco
 

if __name__ == "__main__":
    print "-- Initiative Helper --".center(80)
    
    session = Session()
    command_dict = {'next_encounter': session.next_encounter,
                    'print_init': session.print_current_enc,
                    'save': session.save,
                    'new_players': session.new_players}
    
    Commandline(command_dict).loop()
