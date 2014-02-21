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
        M.DamageType('Acid',
                     'Corrosive liquid'),
        M.DamageType('Cold',
                     'Ice crystals, arctic air, or frigid liquid'),
        M.DamageType('Fire',
                     'Explosive bursts, fiery rays, or simple ignition'),
        M.DamageType('Force',
                     'Invisible energy formed into incredibly hard, '
                     'yet nonsolid shapes'),
        M.DamageType('Lightning',
                     'Electrical energy'),
        M.DamageType('Necrotic',
                     'Purple-black energy that deadens flesh '
                     'and wounds the soul'),
        M.DamageType('Poison',
                     "Toxins that reduce a creature's hit points"),
        M.DamageType('Psychic',
                     'Effects that target the mind'),
        M.DamageType('Radiant',
                     'Searing white light or shimmering colors'),
        M.DamageType('Thunder',
                     'Shock waves and deafening sounds'),
    ])
    session.add_all([
        M.Alignment(name='Lawful Good', good=True, lawful=True),
        M.Alignment(name='Good', good=True),
        M.Alignment(name='Unaligned'),
        M.Alignment(name='Evil', evil=True),
        M.Alignment(name='Chaotic Evil', evil=True, chaotic=True),
    ])
    cleric = M.Class('Cleric', 'Divine', 'Leader')
    fighter = M.Class('Fighter', 'Martial', 'Defender', surges=9)
    paladin = M.Class('Paladin', 'Divine', 'Defender', surges=10)
    ranger = M.Class('Ranger', 'Martial', 'Striker', surges=6)
    rogue = M.Class('Rogue', 'Martial', 'Striker', surges=6)
    warlock = M.Class('Warlock', 'Arcane', 'Striker', surges=6)
    warlord = M.Class('Warlord', 'Martial', 'Leader')
    wizard = M.Class('Wizard', 'Arcane', 'Controller', surges=6)
    avenger = M.Class('Avenger', 'Divine', 'Striker')
    barbarian = M.Class('Barbarian', 'Primal', 'Striker', surges=8)
    bard = M.Class('Bard', 'Arcane', 'Leader')
    druid = M.Class('Druid', 'Primal', 'Controller')
    invoker = M.Class('Invoker', 'Divine', 'Controller', surges=6)
    shaman = M.Class('Shaman', 'Primal', 'Leader')
    sorcerer = M.Class('Sorcerer', 'Arcane', 'Striker', surges=6)
    warden = M.Class('Warden', 'Primal', 'Defender', surges=9)
    session.add_all([cleric, fighter, paladin, ranger, rogue, warlock, warlord,
                     wizard, avenger, barbarian, bard, druid, invoker, shaman,
                     sorcerer, warden])

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
    session.add_all([
        M.Skill('Acrobatics', M.DEX, armor_penalty=True),
        M.Skill('Arcana', M.INT),
        M.Skill('Athletics', M.STR, armor_penalty=True),
        M.Skill('Bluff', M.CHA),
        M.Skill('Diplomacy', M.CHA),
        M.Skill('Dungeoneering', M.WIS),
        M.Skill('Endurance', M.CON, armor_penalty=True),
        M.Skill('Heal', M.WIS),
        M.Skill('History', M.INT),
        M.Skill('Insight', M.WIS),
        M.Skill('Intimidate', M.CHA),
        M.Skill('Nature', M.WIS),
        M.Skill('Perception', M.WIS),
        M.Skill('Religion', M.INT),
        M.Skill('Stealth', M.DEX, armor_penalty=True),
        M.Skill('Streetwise', M.CHA),
        M.Skill('Thievery', M.DEX, armor_penalty=True),
    ])
    session.add_all([
        M.Language(name='Common', script='Common'),
        M.Language(name='Deep Speech', script='Rellanic'),
        M.Language(name='Draconic', script='Iokharic'),
        M.Language(name='Dwarven', script='Davek'),
        M.Language(name='Elven', script='Rellanic'),
        M.Language(name='Giant', script='Davek'),
        M.Language(name='Goblin', script='Common'),
        M.Language(name='Primordial', script='Barazhad'),
        M.Language(name='Supernal', script='Supernal'),
        M.Language(name='Abyssal', script='Barazhad'),
    ])
    deva = M.Race(
        'Deva',
        effect=M.Effect(
            'Deva Racial Benefits',
            intelligence=+2,
            wisdom=+2,
            speed=6,
            vision='Normal',
            stats=[
                M.SkillStat('History', +2),
                M.SkillStat('Religion', +2),
                M.LanguageStat('Common'),
            ]))
    dragonborn = M.Race(
        'Dragonborn',
        effect=M.Effect(
            'Dragonborn Racial Benefits',
            strength=+2,
            charisma=+2,
            vision='Normal',
            speed=6,
            stats=[
                M.SkillStat('History', +2),
                M.SkillStat('Intimidate', +2),
                M.LanguageStat('Common'),
                M.LanguageStat('Draconic'),
            ]))
    dwarf = M.Race(
        'Dwarf',
        effect=M.Effect(
            'Dwarf Racial Benefits',
            constitution=+2,
            wisdom=+2,
            vision='Low-Light',
            speed=5,
            stats=[
                M.SkillStat('Dungeoneering', +2),
                M.SkillStat('Endurance', +2),
                M.LanguageStat('Common'),
                M.LanguageStat('Dwarven'),
            ]))
    eladrin = M.Race(
        'Eladrin',
        effect=M.Effect(
            'Eladrin Racial Benefits',
            dexterity=+2,
            intelligence=+2,
            vision='Low-Light',
            speed=6,
            stats=[
                M.SkillStat('History', +2),
                M.SkillStat('Arcana', +2),
                M.LanguageStat('Common'),
                M.LanguageStat('Elven'),
            ]))
    elf = M.Race(
        'Elf',
        effect=M.Effect(
            dexterity=+2,
            wisdom=+2,
            vision='Low-Light',
            speed=7,
            stats=[
                M.SkillStat('Nature', +2),
                M.SkillStat('Perception', +2),
                M.LanguageStat('Common'),
                M.LanguageStat('Elven'),
            ]))
    half_elf = M.Race(
        'Half-elf',
        effect=M.Effect(
            constitution=+2,
            charisma=+2,
            vision='Low-Light',
            speed=6,
            stats=[
                M.SkillStat('Diplomacy', +2),
                M.SkillStat('Insight', +2),
                M.LanguageStat('Common'),
                M.LanguageStat('Elven'),
            ]))
    halfling = M.Race(
        'Halfling',
        sizename='Small',
        effect=M.Effect(
            dexterity=+2,
            charisma=+2,
            vision='Normal',
            speed=6,
            stats=[
                M.SkillStat('Acrobatics', +2),
                M.SkillStat('Thievery', +2),
                M.LanguageStat('Common'),
            ]))
    human = M.Race(
        'Human'
        effect=M.Effect(
            vision='Normal',
            speed=6,
            stats=[
                M.LanguageStat('Common'),
            ]))
    tiefling = M.Race(
        'Tiefling',
        effect=M.Effect(
            intelligence=+2,
            charisma=+2,
            vision='Low-Light',
            speed=6,
            stats=[
                M.SkillStat('Bluff', +2),
                M.SkillStat('Stealth', +2),
                M.LanguageStat('Common'),
            ]))
    gnome = M.Race(name='Gnome', vision='Low-Light', speed=5, sizename='Small')
    goliath = M.Race(name='Goliath')
    half_orc = M.Race(name='Half-Orc', vision='Low-Light')
    longtooth_shifter = M.Race(name='Longtooth Shifter', vision='Low-Light')
    razorclaw_shifter = M.Race(name='Razorclaw Shifter', vision='Low-Light')
    session.add_all([deva, dragonborn, dwarf, eladrin, elf, half_elf, halfling,
                     human, tiefling, gnome, goliath, half_orc,
                     longtooth_shifter, razorclaw_shifter])


def get_session(db_name):
    '''Easily obtains a session'''
    engine = setup_db(db_name)
    return sessionmaker(bind=engine)()


if __name__ == '__main__':
    sess = get_session('test1.db')
    initialize_database(sess)
    sess.commit()
