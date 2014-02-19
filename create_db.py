from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models as M

import logging

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.basicConfig()


def setup_db(db_filename):
    '''Creates and populates the sqlite database. Nothing will be done if it
    exists and the tables are already defined'''
    engine = create_engine("sqlite:///{}".format(db_filename))
    M.Base.metadata.create_all(bind=engine)
    return engine


def initialize_database(session):
    '''Sets up all reference tables'''
    session.add_all([
        M.Size(name='Tiny', space=0.5),
        M.Size(name='Small', space=1),
        M.Size(name='Medium', space=1),
        M.Size(name='Large', space=2),
        M.Size(name='Huge', space=3),
        M.Size(name='Gargantuan', space=4),
    ])
    session.add_all([
        M.Alignment(name='Lawful Good', good=True, lawful=True),
        M.Alignment(name='Good', good=True),
        M.Alignment(name='Unaligned'),
        M.Alignment(name='Evil', evil=True),
        M.Alignment(name='Chaotic Evil', evil=True, chaotic=True),
    ])
    session.add_all([
        M.Class('Cleric', 'Divine', 'Leader'),
        M.Class('Fighter', 'Martial', 'Defender'),
        M.Class('Paladin', 'Divine', 'Defender'),
        M.Class('Ranger', 'Martial', 'Striker'),
        M.Class('Rogue', 'Martial', 'Striker'),
        M.Class('Warlock', 'Arcane', 'Striker'),
        M.Class('Warlord', 'Martial', 'Leader'),
        M.Class('Wizard', 'Arcane', 'Controller'),
        M.Class('Avenger', 'Divine', 'Striker'),
        M.Class('Barbarian', 'Primal', 'Striker'),
        M.Class('Bard', 'Arcane', 'Leader'),
        M.Class('Druid', 'Primal', 'Controller'),
        M.Class('Invoker', 'Divine', 'Controller'),
        M.Class('Shaman', 'Primal', 'Leader'),
        M.Class('Sorcerer', 'Arcane', 'Striker'),
        M.Class('Warden', 'Primal', 'Defender'),
    ])
    session.add_all([
        M.Race(name='Dragonborn'),
        M.Race(name='Dwarf', vision='Low-Light', speed=5),
        M.Race(name='Eladrin', vision='Low-Light'),
        M.Race(name='Elf', vision='Low-Light', speed=7),
        M.Race(name='Half-elf', vision='Low-Light'),
        M.Race(name='Halfling', sizename='Small'),
        M.Race(name='Human'),
        M.Race(name='Tiefling', vision='Low-Light'),
        M.Race(name='Deva'),
        M.Race(name='Gnome', vision='Low-Light', speed=5, sizename='Small'),
        M.Race(name='Goliath'),
        M.Race(name='Half-Orc', vision='Low-Light'),
        M.Race(name='Longtooth Shifter', vision='Low-Light'),
        M.Race(name='Razorclaw Shifter', vision='Low-Light'),
    ])
    session.add_all([
        M.Deity(name='Avandra',
                alignmentname='Good',
                domains=['Change',
                         'Luck',
                         'Travel'],
                patron_of='Halfling'),
        M.Deity(name='Bahamut',
                alignmentname='Lawful Good',
                domains=['Justice',
                         'Protection',
                         'Nobility'],
                patron_of='Dragonborn'),
        M.Deity(name='Moradin',
                alignmentname='Lawful Good',
                domains=['Family',
                         'Community',
                         'Creation'],
                patron_of='Dwarf'),
        M.Deity(name='Pelor',
                alignmentname='Good',
                domains=['Sun',
                         'Agriculture',
                         'Time'],
                season='Summer'),
        M.Deity(name='Corellon',
                alignmentname='Unaligned',
                domains=['Beauty',
                         'Art',
                         'Magic',
                         'The Fey'],
                patron_of='Eladrin',
                season='Spring'),
        M.Deity(name='Erathis',
                alignmentname='Unaligned',
                domains=['Civilization',
                         'Inventions',
                         'Law']),
        M.Deity(name='Ioun',
                alignmentname='Unaligned',
                domains=['Knowledge',
                         'Skill',
                         'Prophecy']),
        M.Deity(name='Kord',
                alignmentname='Unaligned',
                domains=['Storms',
                         'Battle',
                         'Strength']),
        M.Deity(name='Melora',
                alignmentname='Unaligned',
                domains=['Wilderness',
                         'Nature',
                         'Sea']),
        M.Deity(name='Raven Queen',
                alignmentname='Unaligned',
                domains=['Death',
                         'Fate',
                         'Doom'],
                season='Winter'),
        M.Deity(name='Sehanine',
                alignmentname='Unaligned',
                domains=['Illusion',
                         'Love',
                         'The Moon'],
                season='Autumn',
                patron_of='Elf'),
        M.Deity(name='Asmodeus',
                alignmentname='Evil',
                domains=['Tyranny',
                         'Domination']),
        M.Deity(name='Bane',
                alignmentname='Evil',
                domains=['War', 'Conquest']),
        M.Deity(name='Gruumsh',
                alignmentname='Chaotic Evil',
                domains=['Slaughter', 'Destruction']),
        M.Deity(name='Lolth',
                alignmentname='Chaotic Evil',
                domains=['Shadow', 'Lies']),
        M.Deity(name='Tharizdun'),
        M.Deity(name='Tiamat',
                alignmentname='Evil',
                domains=['Greed', 'Envy']),
        M.Deity(name='Torog',
                alignmentname='Evil',
                domains=['The Underdark']),
        M.Deity(name='Vecna',
                alignmentname='Evil',
                domains=['The Undead', 'Necromancy']),
        M.Deity(name='Zehir',
                alignmentname='Evil',
                domains=['Darkness', 'Poison']),
    ])


def get_session(db_name):
    '''Easily obtains a session'''
    engine = setup_db(db_name)
    return sessionmaker(bind=engine)()


if __name__ == '__main__':
    sess = get_session('test1.db')
    initialize_database(sess)
    sess.commit()
