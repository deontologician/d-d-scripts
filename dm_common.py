import random as r
import readline


class Character(object):
    def __init__(self, name, init_mod=0, max_hp=0):
        self.name = name
        self.init_mod = init_mod
        self.effects = []
        self.max_hp = max_hp
        self.hp = max_hp

    @property
    def json(self):
        output = {
            'name': self.name,
            'init_mod': self.init_mod,
            'effects': [e.json for e in self.effects],
            'max_hp': self.max_hp,
            'hp': self.hp,
        }

    def damage(self, dmg):
        "Simulates damage to monster"
        self.hp -= dmg

    def life_status(self):
        "Whether bloodied/disabled/dying/dead"
        if self.bloodied:
            return "bloodied"
        elif self.disabled:
            return "disabled"
        elif self.dying:
            return "dying"
        elif self.dead:
            return "dead"
        else:
            return ""

    @property
    def bloodied(self):
        return self.max_hp//2 >= self.hp

    @property
    def dead(self):
        return self.hp <= -10

    @property
    def disabled(self):
        return self.hp == 0

    @property
    def dying(self):
        return -10 < self.hp < 0

    def status(self):
        "Returns a string of the current status"
        return self.name + ": (" + str(self.hp) + "/"\
            + str(self.max_hp) + ")hp "\
            + ('(' + self.life_status() + ')' if self.life_status() else "")\
            + ("[" + "][".join(self.effects) + "]" if self.effects else "")

    def __repr__(self):
        return self.name

    def affect(self, effect):
        "Adds a status effect string"
        self.effects.append(effect)
    
    def defect(self, effect):
        "Removes a status effect string"
        self.effects.remove(effect)
    

class PlayerCharacter(Character):
    def __init__(self, *args, **kwargs):
        self.playername = kwargs.pop('playername', None)
        super(PlayerCharacter, self).__init__(*args, **kwargs)

    @property
    def json(self):
        parent = super(PlayerCharacter, self).json
        parent['playername'] = self.playername
        return parent


class Monster(Character):
    '''A Monster'''

    def __init__(self, *args, **kwargs):
        self.encounter = kwargs.pop('encounter', None)
        super(Monster, self).__init__()

    @property
    def dying(self):
        return False

    @property
    def disabled(self):
        return False

    @property
    def dead(self):
        return self.hp <= 0

class Completer(object):
    "This keeps a list of the possible keywords for autocompletion"
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []

    def __enter__(self):
        self.old_completer = readline.get_completer()
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)

    def __exit__(self, *args, **kwargs):
        readline.set_completer(self.old_completer)
        
    def complete(self, text, state):
        "This is called by the readline module"
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

class Commandline(object):
    "A command line useful for different scripts"
    def __init__(self, command_dict):
        self.commands = command_dict
        
    def reset_completer(self):
        Completer(self.commands.keys() + ['exit','help'])

    def loop(self):
        "Call this to start the command loop"
        print 'type "help" for help'
        while True:
            try:
                self.reset_completer() # commands can add their own
                                       # completers
                cmd = raw_input("cmd> ").strip().lower().split()[0]
                if cmd == 'exit':
                    print "Bye"
                    break
                elif cmd == 'help':
                    print self.help()
                else:
                    try:
                        self.commands[cmd]()
                    except KeyError:
                        print "Command not recognized."
            except Exception as exp:
                print exp
                #print "Nope."

    def help(self):
        "Gets a string of the available commands"
        help_string = "Commands: "
        for cmd in sorted(self.commands.keys()):
            help_string += cmd + ", "
        help_string += "help, exit"
        return help_string


def ordinal(num):
    "Returns the number passed in with the correct ordinal suffix"
    ones_place = num % 10
    tens = num % 100
    if ones_place == 1:
        if tens == 11:
            suffix = "th"
        else:
            suffix = "st"
    elif ones_place == 2:
        if tens == 12:
            suffix = "th"
        else:
            suffix = "nd"
    elif ones_place == 3:
        if tens == 13:
            suffix = "th"
        else:
            suffix = "rd"
    else:
        suffix = "th"
    return "%d%s" % (num,suffix)

def letterer(num):
    "Creates a unique letter sequence for each number passed in"
    if num < 0:
        raise ArithmeticError("Number must be 0 or greater")
    if num == 0:
        return ""
    num = num - 1
    letters = chr(ord('A') + (num % 26))
    while num > 25:
        num = num / 26 - 1
        letters = chr(ord('A')+(num % 26)) + letters
    return letters
        
        
# Dice rolls

def d20():
    "Simulates a d20 roll"
    return r.randint(1,20)

def d12():
    "Simulates a d12 roll"
    return r.randint(1,12)

def d10():
    "Simulates a d10 roll"
    return r.randint(1,10)

def d8():
    "Simulates a d8 roll"
    return r.randint(1,8)

def d6():
    "Simulates a d6 roll"
    return r.randint(1,6)

def d4():
    "Simulates a d4 roll"
    return r.randint(1,4)

def d2():
    "Simulates a d2 roll"
    return r.randint(1,2)

def ability_rolls():
    rolls = [sum(sorted(r.randint(1, 6)
                        for _ in xrange(4))[1:])
                        for _x in xrange(6)]
    avg = sum(rolls) / float(len(rolls))
    return rolls, avg
