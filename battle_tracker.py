from __future__ import print_function
from time import strftime
from random import choice, sample
import cmd
import shlex
import functools
import json
import string

from dm_common import (d20, PlayerCharacter, Monster, Commandline, ordinal,
                       letterer, Completer)


def fprint(template, *args, **kwargs):
    '''Prints a formatted string given the later arguments'''
    print(template.format(*args, **kwargs))


def rand_string(l=5):
    '''Return a random string of length l'''
    return ''.join(sample(string.ascii_letters, l))


def keep_asking(prompt, validator=None):
    '''Keep asking the prompt in a loop until the user gives a valid answer.
    `validator` should raise a ValueError if the value is incorrect
    '''
    validator = validator or (lambda x: x)
    while True:
        try:
            return validator(raw_input(prompt))
        except ValueError as e:
            fprint('Invalid input: {}', e)


class Session(object):
    "A series of encounters "
    def __init__(self, name=None):
        self.date = strftime("%A %B %d, %Y %I:%M %p")
        if name is None:
            name = 'Unnamed Session [{}]'.format(rand_string())
        self.name = name
        self.encounters = []
        self.players = []
        return
        self.new_players()
        self.next_encounter()

    def add_encounter(self):
        "Adds a new encounter to the encounter list"
        encounter = Encounter(session=self)
        self.encounters.append(encounter)
        return encounter

    def __repr__(self):
        pieces = [self.name, self.date]
        pieces.extend(str(enc) for enc in self.encounters)
        return "\n".join(pieces)

    @property
    def encounter(self):
        "Get the current encounter"
        return self.encounters[-1] if self.encounters else None

    def save(self):
        "Saves the session to a readable file"
        default_name = self.name.title().replace(" ","") + ".txt"
        filename = raw_input("Filename (default '%s'): "\
                                 % default_name).strip()
        if filename == "":
            filename = default_name
        with open(filename,'w') as f:
            f.write(str(self))
        print("Encounter saved to %s " % filename)

    def damage(self):
        "Damages a monster"
        monsters = self.curr_enc().monsters
        valid_mons = [mon.name for mon in monsters]
        with Completer(valid_mons):
            print("Which Monster gets the damage?")
            print("\n".join([mon.name for mon in monsters]))
            monster_name = raw_input("Name: ")

        for mnstr in monsters:
            if mnstr.name == monster_name:
                monster = mnstr
                break
        else:
            print("No monster with that name.")
            return
        monster.damage(int(raw_input("How much damage?: ")))

    def print_mon_status(self):
        "Prints the status of all Monsters"
        print("<<Monster Status'>>".center(80))
        print("\n".join([mon.status() for mon in self.curr_enc().monsters]))

    def affect(self):
        monsters = self.curr_enc().monsters
        valid_mons = [mon.name for mon in monsters]
        with Completer(valid_mons):
            print("Which Monster gets affected?")
            print("\n".join(valid_mons))
            monster_name = raw_input("Name: ")
        
        for mon in monsters:
            if mon.name == monster_name:
                monster = mon
                break
        else:
            print("No monster with that name")
            return
        monster.affect(raw_input("What is the effect?: "))

    def defect(self):
        "Removes an affect from a monster"
        monsters = self.curr_enc().monsters
        valid_mons = [mon.name for mon in monsters if mon.effects]
        if not valid_mons:
            print("No monsters have effects currently.")
            return

        with Completer(valid_mons):
            print("Which monster's effect is gone?")
            print("\n".join(valid_mons))
            monster_name = raw_input("Name: ")
        for monster in monsters:
            if monster.name == monster_name:
                break
        else:
            print("No monster with that name")
            return

        with Completer(monster.effects):
            print("Which effect needs to be removed?")
            print("\n".join(monster.effects))
            monster.defect(raw_input("Effect: "))


class Encounter(object):
    "Simulates an encounter given a player and monster list"

    def __init__(self, name=None, session=None):
        if name is None:
            name = 'Encounter [{}]'.format(rand_string())
        self.name = name
        self.session = session
        self.p_mod = 0
        self.m_mod = 0
        self.initiative_order = []
        self.players = self.session.players
        self.monsters = []
        self.roll_initiative()

    def roll_initiative(self):
        "Rolls the initiative and creates the initiative order"
        self.initiative_order.extend([(d20() + plyr.init_mod + self.p_mod,
                                plyr) for plyr in self.players])

        self.initiative_order.extend([(d20() + mnstr.init_mod + self.m_mod,
                                mnstr) for mnstr in self.monsters])

        self.initiative_order.sort(cmp=init_comparer)

    def add_monster(self, mon):
        self.monsters.append(mon)
        mon.encounter = self

    def add_monsters(self, amount, monster_type, init_mod, hp):
        '''Add multiple monsters of the same type'''
        if amount == 1:  # special case, ignore auto-lettering
            self.add_monster(Monster(monster_type, init_mod, hp))
            return
        for designation in map(letterer, xrange(amount)):
            self.add_monster(
                Monster(monster_type + " " + designation, init_mod, hp))

    def __repr__(self):
        title_bar = "-[{0.name}]-".format(self).center(80)
        init_template = '{init} -> "{name}" {status}'
        initiative = "\n".join(init_template.format(
            init=init,
            name=character.name,
            status=character.life_status(),
            ) for (init, character) in self.initiative_order)
        return "{title_bar}\n{initiative}\n".format(
            title_bar=title_bar, initiative=initiative)


def init_comparer((total_initA, A), (total_initB, B)):
    "Compares two (init, PlayerCharacter) tuples for precedence"
    if total_initA > total_initB:
        return -1
    elif total_initA < total_initB:
        return 1
    else:  # absolute inits are the same, get the highest mod
        if A.init_mod > B.init_mod:
            return -1
        elif A.init_mod < B.init_mod:
            return 1
        else:
            if id(A) > id(B):
                return -1
            elif id(A) < id(B):
                return 1
            else:
                return 0


def print_wrap(func):
    return lambda *args, **kwargs: print(func(*args, **kwargs))

def new_encounter(players):
    enc_name = raw_input("Encounter name: ")
    p_init = int(raw_input("Enter situational init modifier"\
                               " for the players:"))
    m_init = int(raw_input("Enter situational init modifier"\
                               " for the monsters:"))
    enco = Encounter(enc_name, players, player_mod = p_init, 
                     monster_mod = m_init)
    print("Ok, here is the encounter initiative order:")
    print(enco)
    return enco


def shlexify(func):
    @functools.wraps(func)
    def shlex_wrap(self, args):
        arglist = shlex.split(args)
        return func(self, *arglist)
    return shlex_wrap


def requires_session(func):
    @functools.wraps(func)
    def session_wrap(self, *args, **kwargs):
        if self.session is None:
            fprint('No active session! Create one with the `session` command')
        else:
            return func(self, *args, **kwargs)
    return session_wrap


def requires_players(func):
    @functools.wraps(func)
    @requires_session
    def players_wrap(self, *args, **kwargs):
        if not self.players:
            fprint('No players yet! Add some with the `players` command')
        else:
            return func(self, *args, **kwargs)
    return players_wrap


def requires_encounter(func):
    @functools.wraps(func)
    @requires_players
    def encounter_wrap(self, *args, **kwargs):
        if not self.encounters:
            fprint('No encounter active! Create an encounter with `encounter`')
        else:
            return func(self, *args, **kwargs)
    return encounter_wrap


class BattleCmd(cmd.Cmd):
    '''The command line class'''

    prompt = 'BT> '

    def __init__(self):
        self.session = Session()
        self.session.add_encounter()
        self.encounters = self.session.encounters
        self.players = self.session.players
        cmd.Cmd.__init__(self)

    def cmdloop(self):
        '''Override command loop to abort on Ctrl+C'''
        while True:
            try:
                return cmd.Cmd.cmdloop(self)
            except KeyboardInterrupt:
                continue

    def do_EOF(self, args):
        return True

    def do_session(self, args):
        '''Several subcommands on the session

        Create a new session:
        BT> session new [<SESSION_NAME>]
        Rename the current session:
        BT> session name <SESSION_NAME>
        '''
        arglist = shlex.split(args)
        if not arglist:
            return print(self.session)
        subcommand = arglist.pop(0)
        if subcommand == 'new':
            self.session = Session(name=args[0] if args else None)
        elif subcommand == 'name':
            self.session.name = Session(name=args[0])
        else:
            fprint('Command `{}` not recognized', subcommand)

    @requires_session
    @shlexify
    def do_players(self, *args):
        '''Operate on the players

        Print the list of players:
        BT> players
        Walk through adding new players:
        BT> players new
        Add a single player
        BT> players add <PLAYER_NAME>
        '''
        args = list(args)
        if not args:
            if not self.players:
                print('No players currently!')
            else:
                print('\n'.join(str(p) for p in self.players))
            return
        subcommand = args.pop(0)
        if subcommand == 'new':
            return self.interactive_player_creation()
        elif subcommand == 'add':
            name = args.pop(0)
            self.players.append(PlayerCharacter(name, ))

    def interactive_player_creation(self):
        '''Walks through creating players'''
        num_players = int(raw_input("How many players are there? "))
        for i in xrange(num_players):
            name = raw_input("%s player's name: " % ordinal(i+1)).strip()
            init = keep_asking("{}'s initiative modifier: ".format(name), int)
            self.players.append(PlayerCharacter(name, init))

    def new_monsters(self):
        "Creates new monsters from the command line"

        while True:
            mon_name = raw_input("Monster name: ").title()
            mon_num = keep_asking("Number of {}(s): ".format(mon_name), int)
            mon_init = keep_asking(mon_name + " initiative modifier: ", int)
            mon_hp = keep_asking(mon_name + " hp: ", int)
            self.encounter.add_monsters(mon_num, mon_name, mon_init, mon_hp)
            with Completer(["yes", "no"]):
                more = raw_input("More monster types?[yN] ").strip().lower()
            if more.startswith("n"):
                print(self.monsters)
                break

    @requires_players
    def do_encounter(self, *name):
        '''Operate on the encounter'''
        self.new_monsters()



if __name__ == "__main__":
    print("-- Battle Tracker --".center(80))
    bt = BattleCmd()
    bt.cmdloop()
    # session = Session()
    # command_dict = {'next': session.next_encounter,
    #                 'print_init': session.print_current_enc,
    #                 'save': session.save,
    #                 'new_players': session.new_players,
    #                 'dmg': session.damage,
    #                 'monstatus': session.print_mon_status,
    #                 'roll': make_printer(d20),
    #                 'affect': session.affect,
    #                 'defect': session.defect}
    # Commandline(command_dict).loop()
