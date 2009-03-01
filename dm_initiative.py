try:
    import readline
except:
    pass
from dm_common import *

def mml(mon_type, num, init_mod):
    "Quickly creates a list of monsters of the given quantity"
    mon_list = []
    for pl in xrange(num):
        mon = Player(mon_type + " " + chr(ord('A')+pl), init_mod)
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

def new_monsters():
    "Creates new monsters from the command line"
    ret_list = []
    more = "yes"
    while more != "no":
        mon_name = raw_input("Monster name: ").title()
        mon_num = int(raw_input("Number of %s(s): " % mon_name))
        mon_init = int(raw_input("%s initiative: " % mon_name))
        ret_list.extend(mml(mon_name, mon_num, mon_init))
        more = raw_input("More monster types? (yes/no)").strip().lower()
    return ret_list
    
def new_encounter(plist, mlist):
    p_init = int(raw_input("Enter situational init modifier"\
                               " for the players:"))
    m_init = int(raw_input("Enter situational init modifier"\
                               " for the monsters:"))
    enc = Encounter(plist, mlist, p_init, m_init)
    print "Ok, here is the encounter initiative order:"
    print enc
    return enc

class Completer(object):
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []
        
    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response
    

if __name__ == "__main__":
    print "-- Initiative Helper --".center(80)
    num_players = int(raw_input("How many players are there? "))
    player_list = []
    for i in xrange(num_players):
        name = raw_input("Player's name: ")
        init = int(raw_input("%s's initiative modifier: " % name))
        player_list.append(Player(name, init))

    monster_list = []
    encounter = None
    command_list = ['help','new_monsters','new_encounter', 'print_init',
                    'exit']
    completer = Completer(command_list)
    print 'type "help" for help'
    readline.set_completer(completer.complete) # add tab completion options
    readline.parse_and_bind("tab: complete") # add tab completion
    while True:
        inn = raw_input("Command : ").strip().lower()
        if inn == "help":
            print "Commands: ",
            for s in command_list:
                print s + ",",
            print ""
        elif inn == "new_monsters":
            monster_list = new_monsters()
        elif inn == "new_encounter":
            encounter = new_encounter(player_list, monster_list)
        elif inn == "save":
            if encounter:
                savefile(encounter)
            else:
                print "Nothing to save."
        elif inn == "print_init":
            try:
                print encounter
            except:
                print 'No encounter yet, type "new_encounter"'
        elif inn == "exit":
            print "Bye"
            break
        else:
            print "No such command"
