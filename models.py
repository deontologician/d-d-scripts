from sqlalchemy import (Column, Integer, String, Float, ForeignKey, Boolean,
                        Enum, Date, Table, Index, inspect)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list

DeclBase = declarative_base()

STR = 'Strength'
CON = 'Constitution'
DEX = 'Dexterity'
INT = 'Intelligence'
WIS = 'Wisdom'
CHA = 'Charisma'

AbilityType = Enum(STR, CON, DEX, INT, WIS, CHA)


def pretty(attrname):
    '''Converts and attribute name to a user visible string'''
    return attrname.replace('_', ' ').title()


def pytype(column):
    '''Gets the python type of a column'''
    return column.type.python_type()


class Base(DeclBase):
    '''Common functionality'''
    __abstract__ = True

    def __repr__(self):
        tpl = '{classname}:({name})'
        return tpl.format(classname=self.__class__.__name__, name=self.name)


class Size(Base):
    '''Size classes'''
    __tablename__ = 'size'

    name = Column(String, primary_key=True, doc="Size name")
    space = Column(Float,
                   doc="length of side of square this size fills."
                   " e.g. 4 = 4x4")


class Language(Base):
    '''Languages'''
    __tablename__ = 'language'

    name = Column(String, primary_key=True, doc='Name of language')
    script = Column(String, doc='Script language is written in')


class Dice(Base):
    '''Dice types'''
    __tablename__ = 'dice'

    name = Column(String, primary_key=True, doc='Dice name')
    sides = Column(Integer, nullable=False,
                   doc='Number of sides on the die')


class WeaponGroup(Base):
    '''Groups of Weapons'''
    __tablename__ = 'weapongroup'

    name = Column(String, primary_key=True,
                  doc='Name of weapon group')


class WeaponProperty(Base):
    '''Properties Weapons may have'''
    __tablename__ = 'weaponproperty'

    name = Column(String, primary_key=True,
                  doc='Name of weapon property')

    def __init__(self, name):
        self.name = name


class WeaponCategory(Base):
    '''Categories to which a weapon can belong'''
    __tablename__ = 'weaponcategory'

    name = Column(String, primary_key=True,
                  doc='Name of weapon category')
    melee = Column(Boolean, default=False,
                   doc='Weather weapons in this category are melee')
    ranged = Column(Boolean, default=False,
                    doc='Weather weapons in this category are ranged')
    simple = Column(Boolean, default=False,
                    doc='Weather weapons in this category are simple')
    military = Column(Boolean, default=False,
                      doc='Weather weapons in this category are military')
    superior = Column(Boolean, default=False,
                      doc='Weather weapons in this category are superior')
    improvised = Column(Boolean, default=False,
                        doc='Weather weapons in this category are improvised')

    def __init__(self, name, **kwargs):
        self.name = name
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)


weapon_weaponproperty = Table(
    'weapon_weaponproperty',
    Base.metadata,
    Column('weaponname', String, ForeignKey('weapon.name'), primary_key=True),
    Column('propertyname', String,
           ForeignKey('weaponproperty.name'), primary_key=True),
)


class Weapon(Base):
    '''Weapons'''
    __tablename__ = 'weapon'

    name = Column(String, primary_key=True,
                  doc='Name of the weapon')
    proficiency_bonus = Column(
        Integer, default=+2, doc="Bonus to attack if character is proficient")
    dmg_mult = Column(Integer, default=1,
                      doc='Number of dice to roll for damage')
    dicename = Column(String, ForeignKey('dice.name'),
                      doc='Dice to roll for damage')
    groupname = Column(String, ForeignKey('weapongroup.name'),
                       doc='Weapon group this weapon belongs to')
    categoryname = Column(String, ForeignKey('weaponcategory.name'),
                          doc='Category this weapon belongs to')
    handedness = Column(Enum('One-Handed', 'Two-Handed'), default='One-Handed',
                        doc='How many hands this weapon takes to wield'),
    properties = relationship(WeaponProperty,
                              secondary=weapon_weaponproperty,
                              backref='weapons')


class DamageType(Base):
    '''Damage types'''
    __tablename__ = 'damagetype'

    name = Column(String, primary_key=True,
                  doc='Name of damage type')
    description = Column(String, doc='detailed description of the damage type')

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Alignment(Base):
    '''Alignments'''
    __tablename__ = 'alignment'

    name = Column(String, primary_key=True, doc="Alignment Name")
    good = Column(Boolean, default=False,
                  doc="Whether this alignment is good")
    evil = Column(Boolean, default=False,
                  doc="Whether this alignment is evil")
    lawful = Column(Boolean, default=False,
                    doc="Whether this alignment is lawful")
    chaotic = Column(Boolean, default=False,
                     doc="Whether this alignment is chaotic")


class Race(Base):
    '''Character race'''
    __tablename__ = 'race'

    name = Column(String, primary_key=True,
                  doc="Race's name")
    sizename = Column(String, ForeignKey('size.name'),
                      default='Medium',
                      doc="Race's size")
    effectname = Column(String, ForeignKey('effect.name'),
                        doc='Effect of being this race')

    size = relationship(Size)
    patron_deity = relationship('Deity',
                                uselist=False,
                                backref='patron_of_race')
    effect = relationship('Effect')

    def __init__(self, name, **kwargs):
        self.name = name
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)


class_effect = Table(
    'class_effect',
    Base.metadata,
    Column('classname', String, ForeignKey('class.name'), primary_key=True),
    Column('effectname', String, ForeignKey('effect.name'), primary_key=True),
)


class Class(Base):
    '''Character classes'''
    __tablename__ = 'class'
    name = Column(String, primary_key=True, doc="Class name")
    power_source = Column(Enum('Arcane',
                               'Divine',
                               'Martial',
                               'Primal'),
                          doc="Class's power source")
    role = Column(Enum('Leader',
                       'Controller',
                       'Striker',
                       'Defender'),
                  doc="Class's role in a party")
    surges = Column(
        Integer, default=7,
        doc='Number of healing surges this class starts out with')
    effects = relationship('Effect', secondary=class_effect)

    def __init__(self, name, power_source, role, **kwargs):
        self.name = name
        self.power_source = power_source
        self.role = role
        super(Class, self).__init__(**kwargs)


class DeityDomain(Base):
    '''Deity Domains'''
    __tablename__ = 'deity_domain'

    deityname = Column(String, ForeignKey('deity.name'),
                       doc='Deity this domain applies to')
    name = Column(String, primary_key=True, doc='Name of domain')

    def __init__(self, name):
        self.name = name


class Deity(Base):
    '''Deitys'''
    __tablename__ = 'deity'

    name = Column(String, primary_key=True, doc="Deity's name")
    alignmentname = Column(String, ForeignKey('alignment.name'),
                           doc="God's alignment")
    patron_of = Column(String, ForeignKey('race.name'),
                       doc='Race this Deity is a patron of')
    season = Column(Enum('Spring', 'Summer', 'Autumn', 'Winter'),
                    nullable=True,
                    doc="Deity's season (if any)")

    domain_models = relationship(DeityDomain, backref='deity')
    domains = association_proxy('domain_models', 'name')
    alignment = relationship(Alignment)

    def __init__(self, name, alignmentname=None, domains=None,
                 patron_of=None, season=None):
        self.name = name
        self.alignmentname = alignmentname
        if domains:
            self.domains = domains
        self.patron_of = patron_of
        self.season = season


class Character(Base):
    __tablename__ = 'character'

    name = Column(String, primary_key=True, doc="Character's name")
    is_player = Column(Boolean, default=False,
                       doc='Whether this character is controlled by a player')
    racename = Column(String, ForeignKey('race.name'), default='Human',
                      doc="Character's race")
    classname = Column(String, ForeignKey('class.name'),
                       doc="Character's class")
    height = Column(String,
                    doc="Character's height")
    weight = Column(Integer,
                    doc="Character's weight (in lbs)")
    gender = Column(Enum('Female', 'Male', 'Indeterminate'),
                    doc="Character's gender")
    alignmentname = Column(String,
                           ForeignKey('alignment.name'),
                           default='Unaligned',
                           doc="Character's alignment")
    deityname = Column(String, ForeignKey('deity.name'),
                       doc="Character's deity")
    level = Column(Integer, default=1,
                   doc="Character's level")
    max_hp = Column(Integer,
                    doc="Character's maximum permanent hitpoints")
    temporary_hp = Column(Integer, default=0,
                          doc="Character's current temporary hitpoints")
    current_hp = Column(Integer,
                        doc="Character's ")
    action_points = Column(Integer, default=1,
                           doc="Character's current action points")

    strength = Column(Integer, default=10,
                      doc="Character's strength score")
    charisma = Column(Integer, default=10,
                      doc="Character's charisma score")
    constitution = Column(Integer, default=10,
                          doc="Character's constitution score")
    dexterity = Column(Integer, default=10,
                       doc="Character's dexterity score")
    wisdom = Column(Integer, default=10,
                    doc="Character's wisdom score")
    intelligence = Column(Integer, default=10,
                          doc="Character's intelligence score")

    platinum = Column(Integer, default=0, doc='Amount of platinum carried')
    gold = Column(Integer, default=0, doc='Amount of gold carried')
    silver = Column(Integer, default=0, doc='Amount of silver carried')
    copper = Column(Integer, default=0, doc='Amount of copper carried')

    __mapper_args__ = {
        'polymorphic_on': is_player,
    }

    # Relationships
    deity = relationship(Deity)
    class_ = relationship(Class)
    alignment = relationship(Alignment)
    race = relationship(Race)


class Player(Character):
    '''A player controlled character'''
    __mapper_args__ = {
        'polymorphic_identity': True
    }

    playername = Column(String, doc='Name of player who runs this character')
    xp = Column(Integer, doc='Experience points accumulated')


class NPC(Character):
    '''A DM controlled character or monster'''
    __mapper_args__ = {
        'polymorphic_identity': False
    }


class Skill(Base):
    '''Skills a character can have'''
    __tablename__ = 'skill'

    name = Column(String, primary_key=True, doc='Name of this skill')
    ability = Column(AbilityType,
                     doc='Ability score relevant to this skill')
    armor_penalty = Column(
        Boolean, default=False,
        doc='Whether armor penalty can affect this skill')

    def __init__(self, name, ability, armor_penalty=False):
        self.name = name
        self.ability = ability
        self.armor_penalty = armor_penalty


class Effect(Base):
    '''Ongoing effects that apply to characters'''
    __tablename__ = 'effect'

    name = Column(String, primary_key=True,
                  doc='Name of effect')
    max_hp = Column(Integer, doc="Mod to maximum hitpoints")
    intelligence = Column(Integer, doc="Mod to intelligence")
    constitution = Column(Integer, doc="Mod to constitution")
    dexterity = Column(Integer, doc="Mod to dexterity")
    wisdom = Column(Integer, doc="Mod to wisdom")
    charisma = Column(Integer, doc="Mod to charisma")
    strength = Column(Integer, doc="Mod to strength")
    initiative = Column(Integer, doc="Mod to initiative")
    fortitude = Column(Integer, doc="Mod to fortitude")
    will = Column(Integer, doc="Mod to will")
    reflex = Column(Integer, doc="Mod to reflex")
    armor_class = Column(Integer, doc="Mod to armor class")
    speed = Column(Integer, doc="Mod to speed")
    damage = Column(Integer, doc="Mod to damage")
    damage_mult = Column(Float, doc="Multiplier for damage")
    attack_roll = Column(Integer, doc="Mod to attack roll")
    saving_throw = Column(Integer, doc="Mod to saving throw roll")
    healing_surges = Column(Integer, doc="Mod to healing surges")
    vision = Column(Enum('Low-Light',
                         'Darkvision',
                         'Normal',
                         'Blind'),
                    doc="Change vision level to this")

    stats = relationship('Stat', backref='effect')
    languages = relationship('LanguageStat')
    skills = relationship('SkillStat')
    damages = relationship('DamageStat')

    def __init__(self, name, **kwargs):
        self.name = name
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)

    def __str__(self):
        mods = ['{0:+} {1}'.format(getattr(self, attr), pretty(attr))
                for attr, col in inspect(self.__class__).columns.items()
                if attr != 'name'
                and isinstance(pytype(col), int)
                and getattr(self, attr) is not None]
        mods.extend('{} {}'.format(getattr(self, attr), attr.title())
                    for attr, col in inspect(self.__class__).columns.items()
                    if attr != 'name'
                    and isinstance(pytype(col), str)
                    and getattr(self, attr) is not None)
        mods.extend(str(stat) for stat in self.stats)
        return '{0.name}:\n  {1}'.format(self, '\n  '.join(mods))


class Stat(Base):
    '''Multiple stats can be part of a single effect'''

    __tablename__ = 'stat'

    id = Column(Integer, primary_key=True, doc='Unique id of stat')
    effectname = Column(String, ForeignKey('effect.name'),
                        doc='Name of the effect this stat belongs to')
    stat_kind = Column(Enum('language', 'skill', 'damage'),
                       nullable=False,
                       doc='Kind of stat this is')
    __table_args__ = (Index('stat_effectname_idx', effectname),)
    __mapper_args__ = {'polymorphic_on': stat_kind}


class LanguageStat(Stat):
    '''Stat providing language comprehension'''
    __mapper_args__ = {'polymorphic_identity': 'language'}

    language = Column(String, ForeignKey('language.name'),
                      doc="Language understanding bestowed")

    def __init__(self, language):
        self.language = language

    def __repr__(self):
        return 'Understands {}'.format(self.language)


class SkillStat(Stat):
    '''Stat modifying an skill'''
    __mapper_args__ = {'polymorphic_identity': 'skill'}

    skillname = Column(String, ForeignKey('skill.name'),
                       doc="Name of skill modified")
    skill_mod = Column(Integer, doc='Mod to skill amount')

    def __init__(self, skillname, skill_mod):
        self.skillname = skillname
        self.skill_mod = skill_mod

    def __repr__(self):
        return '{0.skill_mod:+} {0.skillname}'.format(self)


class DamageStat(Stat):
    '''Stat modifying a damage type amount'''
    __mapper_args__ = {'polymorphic_identity': 'damage'}

    damagetype_name = Column(String, ForeignKey('damagetype.name'),
                             doc='Damage type resisted/weakened (null if any)')
    damagetype_mod = Column(Integer, doc='Mod to damage type')

    def __init__(self, damagetype_name, damagetype_mod):
        self.damagetype_name = damagetype_name
        self.damagetype_mod = damagetype_mod


class CharacterEncounter(Base):
    '''Links a player to an encounter in initiative order'''
    __tablename__ = 'encounter_init'

    charactername = Column(String, ForeignKey('character.name'),
                           primary_key=True,
                           doc='Character in initiative')
    encounter_id = Column(Integer, ForeignKey('encounter.id'),
                          primary_key=True,
                          doc='Encounter this init roll is for')
    init_score = Column(
        Integer, doc='Initiative rolled for this encounter')
    position = Column(Integer, doc='Current position in the initiative order')
    second_wind = Column(Boolean, default=False,
                         doc='Whether the character still has a '
                             'second wind for this encounter.')

    character = relationship('Character', innerjoin=True, lazy='joined')


class Encounter(Base):
    '''Represents a single encounter'''
    __tablename__ = 'encounter'

    id = Column(Integer, primary_key=True,
                doc="Unique Encounter identifier")
    name = Column(String, doc="Name of Encounter")
    session_id = Column(Integer, ForeignKey('session.id'),
                        doc='Session this encounter belongs to')

    session = relationship('Session', backref='encounters')
    init_order = relationship('CharacterEncounter',
                              order_by='CharacterEncounter.position',
                              lazy='joined',
                              collection_class=ordering_list('position'))
    initiative = association_proxy('init_order', 'character')


class Session(Base):
    '''Play sessions'''
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True,
                doc="Unique session identifier")
    date = Column(Date, doc="date session occurred on")
