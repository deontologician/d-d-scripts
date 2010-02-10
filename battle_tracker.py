import dm_common as dm

from time import strftime
from random import choice

class Session(object):
    "A series of encounters "
    def __init__(self):
        try:
            self.name = raw_input("Name of Session: ").strip()
            self.date = strftime("%A %B %d, %Y %I:%M %p")
            self.encounters = []
            self.plist = []
            self.new_players()
            self.next_encounter()
        except (KeyboardInterrupt, EOFError, ValueError):
            print "\nOK Bye!"
            exit(0)

    @dm.cmddoc("Proceed to the next encounter")
    def next_encounter(self, args = None):
        "Adds a new encounter to the list"
        if args is not None: args = []
        self.encounters.append(new_encounter(self.plist))

    def __repr__(self, args):
        rep = self.name + "\n" + self.date + "\n"
        for i,enco in enumerate(self.encounters):
            rep += "Encounter #%d\n" % (i+1)
            rep += str(enco)
        return rep 

    def curr_enc(self, _args = None):
        "Get the current encounter"
        return self.encounters[-1]

    @dm.cmddoc("Adds new players to the current session")
    def new_players(self, args = None):
        "Makes a new list of characters"
        if args is not None: args = []
        while True:
            try:
                num_players = int(raw_input("How many players are there? "))
                if num_players > 10:
                    sure = raw_input("Are you sure you want %d players?[y/N] " %
                                     num_players)
                    if sure.lower() in ["y","yes"]:
                        break
                    continue
                break
            except ValueError:
                print "Invalid value, try again"
            
        self.plist = []
        for i in xrange(num_players):
            while True:
                try: 
                    name = raw_input("%s player's name: " % dm.ordinal(i+1)).strip()
                    init = int(raw_input("%s's initiative modifier: " % name))
                    self.plist.append(dm.Player(name, init))
                    break
                except ValueError:
                    print "Invalid input. Try again"
                    continue

    @dm.cmddoc("Saves the current session to a file")
    def save(self, args = None):
        "Saves the session to a readable file"
        if args is not None: args = []
        default_name = self.name.title().replace(" ","") + ".txt"
        filename = raw_input("Filename (default '%s'): "\
                                 % default_name).strip()
        if filename == "":
            filename = default_name
        f = open(filename,'w')
        f.write(str(self))
        f.close()
        print "Encounter saved to %s " % filename

    @dm.cmddoc("Damages a monster or a player")
    def damage(self, args = None):
        "Damages a monster"
        if args is not None: args = []
        mlist = self.curr_enc().mlist
        valid_mons = [mon.name for mon in mlist]
        dm.Completer(valid_mons) # add monsters to tab
                                               # completion
        print "Which Monster gets the damage?"
        print "\n".join([mon.name for mon in mlist])
        monster_name = raw_input("Name: ")
        
        for mnstr in mlist:
            if mnstr.name == monster_name:
                monster = mnstr
                break
        else:
            print "No monster with that name."
            return
        monster.damage(int(raw_input("How much damage?: ")))
    
    @dm.cmddoc("Prints a given monster's status")
    def print_mon_status(self, args = None):
        "Prints the status of all Monsters"
        if args is not None: args = []
        print "<<Monster Status'>>".center(80)
        print "\n".join([mon.status() for mon in self.curr_enc().mlist])

    @dm.cmddoc("Adds an effect to a monster or player")
    def affect(self, args = None):
        if args is not None: args = []
        mlist = self.curr_enc().mlist
        valid_mons = [mon.name for mon in mlist]
        dm.Completer(valid_mons) # add monsters to tab
                                               # completion
        print "Which Monster gets affected?"
        print "\n".join(valid_mons)
        monster_name = raw_input("Name: ").strip()
        
        for mon in mlist:
            if mon.name == monster_name:
                monster = mon
                break
        else:
            print "No monster with that name"
            return
        monster.affect(raw_input("What is the effect?: ").strip())

    @dm.cmddoc("Removes an effect from a monster or player")
    def defect(self, args = None):
        "Removes an affect from a monster"
        if args is not None: args = []
        mlist = self.curr_enc().mlist
        valid_mons = [mon.name for mon in mlist if mon.effects]
        if not valid_mons:
            print "No monsters have effects currently."
            return

        dm.Completer(valid_mons) #add monsters to tab completion
        print "Which monster's effect is gone?"
        print "\n".join(valid_mons)
        monster_name = raw_input("Name: ").strip()
        for mon in mlist:
            if mon.name == monster_name:
                monster = mon
                break
        else:
            print "No monster with that name"
            return

        dm.Completer(monster.effects)
        print "Which effect needs to be removed?"
        print "\n".join(monster.effects)
        monster.defect(raw_input("Effect: ").strip())

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
        self.init_list.extend([(dm.d20() + plyr.init_mod + self.p_mod,
                                plyr) for plyr in self.plist])

        self.init_list.extend([(dm.d20() + mnstr.init_mod + self.m_mod,
                                mnstr) for mnstr in self.mlist])

        self.init_list.sort(cmp=init_comparer)

    def __repr__(self):
        ret_string = ("-[%s]-" % self.enc_name).center(80) + "\n"
        ret_string += "\n".join([str(num) + " -> '" + str(name) + "' " + 
                                 name.life_status()
                                 for (num,name) in self.init_list])
        return ret_string + "\n"

    def new_monsters(self):
        "Creates new monsters from the command line"
        self.mlist = []
        def mml(mon_type, num, init_mod, hp):
            if num == 1: #special case, ignore auto-lettering
                self.mlist.append(dm.Monster(mon_type, init_mod, hp))
                return
            for pl in xrange(num):
                      
                mon = dm.Monster(mon_type + " " + dm.letterer(pl+1),
                                 init_mod, hp)
                self.mlist.append(mon)

        while True:
            mon_name = raw_input("Monster name: ").title()
            mon_num = int(raw_input("Number of %s(s): " % mon_name))
            mon_init = int(raw_input("%s initiative modifier: "
                                     % mon_name))
            mon_hp = int(raw_input("%s hp: " % mon_name))
            mml(mon_name, mon_num, mon_init, mon_hp)
            more = raw_input("More monster types? (yes/no) "\
                                 ).strip().lower()
            if more == "yes":
                continue
            else:
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

def make_printer(returner, cmddoc):
    """Returns a function that prints the result of returner, and has the given
    cmddoc"""
    @dm.cmddoc(cmddoc)
    def f(*args, **kwargs):
        print returner(*args, **kwargs)
    return f
      
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
    print "-- Battle Tracker --".center(80)
    
    session = Session()

    print_init = make_printer(session.curr_enc,
                              "Prints the current initiative list")
    roll = make_printer(dm.d20, "Rolls a d20")

    command_dict = {'next': session.next_encounter,
                    'ls': print_init,
                    'save': session.save,
                    'new_players': session.new_players,
                    'dmg': session.damage,
                    'monstatus': session.print_mon_status,
                    'roll': roll,
                    'affect': session.affect,
                    'defect': session.defect}
    
    dm.Commandline(command_dict).loop()
