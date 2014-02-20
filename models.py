from sqlalchemy import (Column, Integer, String, Float, ForeignKey, Boolean,
                        Enum, Date, Table, Index)
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


race_effect = Table(
    'race_effect',
    Base.metadata,
    Column('racename', String, ForeignKey('race.name'), primary_key=True),
    Column('effectname', String, ForeignKey('effect.name'), primary_key=True),
)


class Race(Base):
    '''Character race'''
    __tablename__ = 'race'

    name = Column(String, primary_key=True,
                  doc="Race's name")
    sizename = Column(String, ForeignKey('size.name'),
                      default='Medium',
                      doc="Race's size")
    vision = Column(Enum('Low-Light',
                         'Darkvision',
                         'Normal'),
                    default="Normal",
                    doc="Race's vision-level")
    speed = Column(Integer, default=6,
                   doc="Race's base speed in squares/round")

    size = relationship(Size)

    patron_deity = relationship('Deity',
                                uselist=False,
                                backref='patron_of_race')
    effects = relationship('Effect', secondary=race_effect)


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

    stats = relationship('Stat', innerjoin=True, lazy='joined',
                         backref='effect')


class Stat(Base):
    '''Several stats make up an effect'''

    __tablename__ = 'effectstat'

    id = Column(Integer, primary_key=True, doc='Unique id of effect')
    effectname = Column(String, ForeignKey('effect.name'),
                        doc='Name of this effect this stat belongs to')
    ability = Column(AbilityType, doc='Ability score affected')
    ability_mod = Column(Integer, doc='Mod to ability score')
    max_hp = Column(Integer, doc="Mod to maximum hitpoints")
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

    language = Column(String, ForeignKey('language.name'),
                      doc="Language understanding bestowed")

    skillname = Column(String, ForeignKey('skill.name'),
                       doc="Name of skill modified")
    skill_mod = Column(Integer, doc='Mod to skill amount')

    damagetype_name = Column(String, ForeignKey('damagetype.name'),
                             doc='Damage type resisted/weakened (null if any)')
    damagetype_mod = Column(Integer, doc='Mod to damage type')

    __table_args__ = (Index('effect_name_idx', effectname), )


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
