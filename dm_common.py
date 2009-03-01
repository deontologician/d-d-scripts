import random as r

class Player(object):
    def __init__(self, name, init_mod):
        self.name = name
        self.init_mod = init_mod

    def __repr__(self):
        return self.name

"""Dice rolls"""

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
