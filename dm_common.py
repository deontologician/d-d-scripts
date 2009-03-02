import random as r
import readline

class Player(object):
    def __init__(self, name, init_mod):
        self.name = name
        self.init_mod = init_mod
        self.effects = []

    def __repr__(self):
        return self.name

    def affect(self, effect):
        "Adds a status effect string"
        self.effects.append(effect)
    def life_status(self):
        return ""
        

class Monster(Player):
    def __init__(self, name, init_mod, max_hp):
        Player.__init__(self, name, init_mod)
        self.max_hp = max_hp
        self.hp = max_hp

    def damage(self, dmg):
        "Simulates damage to monster"
        self.hp -= dmg

    def life_status(self):
        "Whether the monster is bloodied or dead"
        if self.hp <= 0:
            return "dead"
        elif self.max_hp/2 >= self.hp:
            return "bloodied"
        else:
            return ""

    def status(self):
        "Returns a string of the current status"
        return '"' + self.name + '" ' + str(self.hp) + "hp "\
            + ('(' + self.life_status() + ')' if self.life_status() else "")\
            + ("[" + "][".join(self.effects) + "]" if self.effects else "")
    

class Completer(object):
    "This keeps a list of the possible keywords for autocompletion"
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)
        
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
        suffix = "st"
    return "%d%s" % (num,suffix)
        

        
        
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
