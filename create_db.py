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
        M.Dice('d4', sides=4),
        M.Dice('d6', sides=6),
        M.Dice('d8', sides=8),
        M.Dice('d10', sides=10),
        M.Dice('d12', sides=12),
        M.Dice('d20', sides=20),
    ])
    session.add_all([
        M.Size('Tiny', space=0.5),
        M.Size('Small', space=1),
        M.Size('Medium', space=1),
        M.Size('Large', space=2),
        M.Size('Huge', space=3),
        M.Size('Gargantuan', space=4),
    ])
    session.add_all([
        M.StatType('Language'),
        M.StatType('Skill'),
        M.StatType('Damage'),
        M.StatType('Proficiency'),
    ])
    session.add_all([
        M.BonusType('Armor'),
        M.BonusType('Enhancement'),
        M.BonusType('Feat'),
        M.BonusType('Item'),
        M.BonusType('Power'),
        M.BonusType('Proficiency'),
        M.BonusType('Racial'),
        M.BonusType('Untyped'),
    ])
    session.add_all([
        M.PowerSource('Martial',
                      'Represents military training or general '
                      'prowess with physical weaponry'),
        M.PowerSource('Divine',
                      'represents that powers come due to a '
                      'connection with a deity or the spiritual realm'),
        M.PowerSource('Arcane', 'Your powers come from magical sources'),
        M.PowerSource('Psionic', 'Your powers are mental'),
        M.PowerSource('Primal', 'Your powers come from a deep connection '
                      'to the world and the spirits'),
        M.PowerSource('Shadow', 'Your powers come form opening a well of '
                      'energy from the Shadowfell')
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
        M.Alignment('Lawful Good', good=True, lawful=True),
        M.Alignment('Good', good=True),
        M.Alignment('Unaligned'),
        M.Alignment('Evil', evil=True),
        M.Alignment('Chaotic Evil', evil=True, chaotic=True),
    ])
    session.add_all([
        M.WeaponGroup('Axe'),
        M.WeaponGroup('Bow'),
        M.WeaponGroup('CrossBow'),
        M.WeaponGroup('Flail'),
        M.WeaponGroup('Hammer'),
        M.WeaponGroup('Heavy Blade'),
        M.WeaponGroup('Light Blade'),
        M.WeaponGroup('Mace'),
        M.WeaponGroup('Pick'),
        M.WeaponGroup('Polearm'),
        M.WeaponGroup('Sling'),
        M.WeaponGroup('Spear'),
        M.WeaponGroup('Staff'),
        M.WeaponGroup('Unarmed'),
    ])
    session.add_all([
        M.WeaponProperty('Heavy Thrown'),
        M.WeaponProperty('High Crit'),
        M.WeaponProperty('Light Thrown'),
        M.WeaponProperty('Load Free'),
        M.WeaponProperty('Load Minor'),
        M.WeaponProperty('Off-Hand'),
        M.WeaponProperty('Reach'),
        M.WeaponProperty('Small'),
        M.WeaponProperty('Versatile'),
    ])
    session.add_all([
        M.WeaponCategory('Simple Melee', simple=True, melee=True),
        M.WeaponCategory('Military Melee', military=True, melee=True),
        M.WeaponCategory('Superior Melee', superior=True, melee=True),
        M.WeaponCategory('Improvised Melee', improvised=True, melee=True),
        M.WeaponCategory('Simple Ranged', simple=True, ranged=True),
        M.WeaponCategory('Military Ranged', military=True, ranged=True),
        M.WeaponCategory('Superior Ranged', superior=True, ranged=True),
        M.WeaponCategory('Improvised Ranged', improvised=True, ranged=True),
    ])
    session.add_all([
        M.ArmorType('Cloth', weight='Light'),
        M.ArmorType('Leather', weight='Light'),
        M.ArmorType('Hide', weight='Light'),
        M.ArmorType('Chainmail', weight='Heavy'),
        M.ArmorType('Scale', weight='Heavy'),
        M.ArmorType('Plate', weight='Heavy'),
    ])
    session.add_all([
        M.Deity('Avandra',
                alignmentname='Good',
                domains=['Change',
                         'Luck',
                         'Travel'],
                patron_of='Halfling'),
        M.Deity('Bahamut',
                alignmentname='Lawful Good',
                domains=['Justice',
                         'Protection',
                         'Nobility'],
                patron_of='Dragonborn'),
        M.Deity('Moradin',
                alignmentname='Lawful Good',
                domains=['Family',
                         'Community',
                         'Creation'],
                patron_of='Dwarf'),
        M.Deity('Pelor',
                alignmentname='Good',
                domains=['Sun',
                         'Agriculture',
                         'Time'],
                season='Summer'),
        M.Deity('Corellon',
                alignmentname='Unaligned',
                domains=['Beauty',
                         'Art',
                         'Magic',
                         'The Fey'],
                patron_of='Eladrin',
                season='Spring'),
        M.Deity('Erathis',
                alignmentname='Unaligned',
                domains=['Civilization',
                         'Inventions',
                         'Law']),
        M.Deity('Ioun',
                alignmentname='Unaligned',
                domains=['Knowledge',
                         'Skill',
                         'Prophecy']),
        M.Deity('Kord',
                alignmentname='Unaligned',
                domains=['Storms',
                         'Battle',
                         'Strength']),
        M.Deity('Melora',
                alignmentname='Unaligned',
                domains=['Wilderness',
                         'Nature',
                         'Sea']),
        M.Deity('Raven Queen',
                alignmentname='Unaligned',
                domains=['Death',
                         'Fate',
                         'Doom'],
                season='Winter'),
        M.Deity('Sehanine',
                alignmentname='Unaligned',
                domains=['Illusion',
                         'Love',
                         'The Moon'],
                season='Autumn',
                patron_of='Elf'),
        M.Deity('Asmodeus',
                alignmentname='Evil',
                domains=['Tyranny',
                         'Domination']),
        M.Deity('Bane',
                alignmentname='Evil',
                domains=['War', 'Conquest']),
        M.Deity('Gruumsh',
                alignmentname='Chaotic Evil',
                domains=['Slaughter', 'Destruction']),
        M.Deity('Lolth',
                alignmentname='Chaotic Evil',
                domains=['Shadow', 'Lies']),
        M.Deity('Tharizdun'),
        M.Deity('Tiamat',
                alignmentname='Evil',
                domains=['Greed', 'Envy']),
        M.Deity('Torog',
                alignmentname='Evil',
                domains=['The Underdark']),
        M.Deity('Vecna',
                alignmentname='Evil',
                domains=['The Undead', 'Necromancy']),
        M.Deity('Zehir',
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
        M.Language('Common', script='Common'),
        M.Language('Deep Speech', script='Rellanic'),
        M.Language('Draconic', script='Iokharic'),
        M.Language('Dwarven', script='Davek'),
        M.Language('Elven', script='Rellanic'),
        M.Language('Giant', script='Davek'),
        M.Language('Goblin', script='Common'),
        M.Language('Primordial', script='Barazhad'),
        M.Language('Supernal', script='Supernal'),
        M.Language('Abyssal', script='Barazhad'),
    ])
    deva = M.Race(
        'Deva',
        effect=M.Effect(
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
        'Half-Elf',
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
        'Human',
        effect=M.Effect(
            vision='Normal',
            speed=6,
            fortitude=+1,
            reflex=+1,
            will=+1,
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
    gnome = M.Race(
        'Gnome',
        sizename='Small',
        effect=M.Effect(
            intelligence=+2,
            charisma=+2,
            vision='Low-Light',
            speed=5,
            stats=[
                M.SkillStat('Arcana', +2),
                M.SkillStat('Stealth', +2),
                M.LanguageStat('Common'),
                M.LanguageStat('Elven'),
            ]))
    goliath = M.Race(
        'Goliath',
        effect=M.Effect(
            strength=+2,
            constitution=+2,
            vision='Normal',
            speed=6,
            stats=[
                M.SkillStat('Athletics', +2),
                M.SkillStat('Nature', +2),
                M.LanguageStat('Common'),
            ]))
    half_orc = M.Race(
        'Half-Orc',
        effect=M.Effect(
            strength=+2,
            dexterity=+2,
            vision='Low-Light',
            speed=6,
            will=+1,
            stats=[
                M.SkillStat('Endurance', +2),
                M.SkillStat('Intimidate', +2),
                M.LanguageStat('Common'),
                M.LanguageStat('Giant'),
            ]))
    longtooth_shifter = M.Race(
        'Longtooth Shifter',
        effect=M.Effect(
            strength=+2,
            wisdom=+2,
            vision='Low-Light',
            speed=6,
            stats=[
                M.SkillStat('Athletics', +2),
                M.SkillStat('Endurance', +2),
                M.LanguageStat('Common'),
            ]))
    razorclaw_shifter = M.Race(
        'Razorclaw Shifter',
        effect=M.Effect(
            strength=+2,
            wisdom=+2,
            vision='Low-Light',
            speed=6,
            stats=[
                M.SkillStat('Acrobatics', +2),
                M.SkillStat('Stealth', +2),
                M.LanguageStat('Common'),
            ]))
    session.add_all([deva, dragonborn, dwarf, eladrin, elf, half_elf, halfling,
                     human, tiefling, gnome, goliath, half_orc,
                     longtooth_shifter, razorclaw_shifter])
    cleric = M.Class(
        'Cleric',
        powersource_name='Divine',
        role='Leader',
        effects=[
            M.Effect(
                'Cleric Class Benefits',
                healing_surges=7,
                stats=[
                    M.ProficiencyStat(M.WeaponCategory('Simple Melee')),
                    M.ProficiencyStat(M.WeaponCategory('Simple Ranged')),
                    M.ProficiencyStat(M.ArmorType('Light')),
                    M.ProficiencyStat(M.ArmorType('Cloth')),
                ]
            )
        ])
    fighter = M.Class(
        'Fighter',
        powersource_name='Martial',
        role='Defender',
        effects=[
            M.Effect(
                'Fighter Class Benefits',
                healing_surges=9
            )
        ])
    paladin = M.Class(
        'Paladin',
        powersource_name='Divine',
        role='Defender',
        effects=[
            M.Effect(
                'Paladin Class Benefits',
                healing_surges=10
            )
        ])
    ranger = M.Class(
        'Ranger',
        powersource_name='Martial',
        role='Striker',
        effects=[
            M.Effect(
                'Ranger Class Benefits',
                healing_surges=6
            )
        ])
    rogue = M.Class(
        'Rogue',
        powersource_name='Martial',
        role='Striker',
        effects=[
            M.Effect(
                'Rogue Class Benefits',
                healing_surges=6
            )
        ])
    warlock = M.Class(
        'Warlock',
        powersource_name='Arcane',
        role='Striker',
        effects=[
            M.Effect(
                'Warlock Class Benefits',
                healing_surges=6
            )
        ])
    warlord = M.Class(
        'Warlord',
        powersource_name='Martial',
        role='Leader',
        effects=[
            M.Effect(
                'Warlord Class Benefits',
                healing_surges=7
            )
        ])
    wizard = M.Class(
        'Wizard',
        powersource_name='Arcane',
        role='Controller',
        effects=[
            M.Effect(
                'Wizard Class Benefits',
                healing_surges=6
            )
        ])
    avenger = M.Class(
        'Avenger',
        powersource_name='Divine',
        role='Striker',
        effects=[
            M.Effect(
                'Avenger Class Benefits',
                healing_surges=7
            )
        ])
    barbarian = M.Class(
        'Barbarian',
        powersource_name='Primal',
        role='Striker',
        effects=[
            M.Effect(
                'Barbarian Class Benefits',
                healing_surges=8
            )
        ])
    bard = M.Class(
        'Bard',
        powersource_name='Arcane',
        role='Leader',
        effects=[
            M.Effect(
                'Bard Class Benefits',
                healing_surges=7
            )
        ])
    druid = M.Class(
        'Druid',
        powersource_name='Primal',
        role='Controller',
        effects=[
            M.Effect(
                'Druid Class Benefits',
                healing_surges=7
            )
        ])
    invoker = M.Class(
        'Invoker',
        powersource_name='Divine',
        role='Controller',
        effects=[
            M.Effect(
                'Invoker Class Benefits',
                healing_surges=6
            )
        ])
    shaman = M.Class(
        'Shaman',
        powersource_name='Primal',
        role='Leader',
        effects=[
            M.Effect(
                'Shaman Class Benefits',
                healing_surges=7
            )
        ])
    sorcerer = M.Class(
        'Sorcerer',
        powersource_name='Arcane',
        role='Striker',
        effects=[
            M.Effect(
                'Sorcerer Class Benefits',
                healing_surges=6
            )
        ])
    warden = M.Class(
        'Warden',
        powersource_name='Primal',
        role='Defender',
        effects=[
            M.Effect(
                'Warden Class Benefits',
                healing_surges=9
            )
        ])
    session.add_all([cleric, fighter, paladin, ranger, rogue, warlock, warlord,
                     wizard, avenger, barbarian, bard, druid, invoker, shaman,
                     sorcerer, warden])
    session.add_all([
        M.Armor('Cloth Armor (basic clothing)', typename='Cloth', weight=4),
        M.Armor('Feyweave Armor', typename='Cloth', weight=5, ac_bonus=+1),
        M.Armor('Starweave Armor', typename='Cloth', weight=3, ac_bonus=+2),
        M.Armor('Leather Armor', typename='Leather', weight=15, ac_bonus=+2),
        M.Armor('Feyleather Armor',
                typename='Leather', weight=15, ac_bonus=+3),
        M.Armor('Starleather Armor',
                typename='Leather', weight=15, ac_bonus=+4),
        M.Armor('Hide Armor',
                typename='Hide', weight=25, check=-1, ac_bonus=+3),
    ])


def get_session(db_name):
    '''Easily obtains a session'''
    engine = setup_db(db_name)
    return sessionmaker(bind=engine)()


def main(filename):
    sess = get_session(filename)
    initialize_database(sess)
    sess.commit()


if __name__ == '__main__':
    main('test1.db')
