import random as r
import readline

class Player(object):
    def __init__(self, name, init_mod):
        self.name = name
        self.init_mod = init_mod

    def __repr__(self):
        return self.name

class Monster(object):
    def __init__(self, name, init_mod, max_hp):
        self.name = name
        self.init_mod = init_mod
        self.max_hp = max_hp
        self.hp = max_hp
        self.effects = []

    def __repr__(self):
        return self.name

    def damage(self, dmg):
        "Simulates damage to monster"
        self.hp -= dmg

    def affected_by(self, effect):
        "Adds a status effect (which is a string)"
        self.effects.append(effect)

    def is_bloodied(self):
        "Whether the monster is bloodied"
        return self.max_hp/2 >= self.hp
    

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
        self.completer = Completer(command_dict.keys() + ['exit','help'])

    def loop(self):
        "Call this to start the command loop"
        print 'type "help" for help'
        while True:
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

    def help(self):
        "Gets a string of the available commands"
        help_string = "Commands: "
        for cmd in sorted(self.commands.keys()):
            help_string += cmd + ", "
        help_string += "help, exit"
        
        
        
        
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
