from collections import Sized, Iterable
from sqlalchemy import (Column, Integer, String, Float, ForeignKey, Boolean,
                        Enum, Date, Table, Index, inspect)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext import associationproxy
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


def JSONColumn(*args, **kwargs):
    '''Adds an info to the Column indicating the attribute should be serialized
    to json'''
    return Column(*args, info={'jsonify': True}, **kwargs)


def jsonrelationship(*args, **kwargs):
    '''Adds an info indicating the relationship should be serialized to json'''
    return relationship(*args, info={'jsonify': True}, **kwargs)


def jsonassociation_proxy(*args, **kwargs):
    '''Adds an info property to an association proxy'''
    ap = association_proxy(*args, **kwargs)
    ap.info = {'jsonify': True}
    return ap


def association_proxy(*args, **kwargs):
    '''Add an info property to association_proxy since one doesn't exist'''
    ap = associationproxy.association_proxy(*args, **kwargs)
    ap.info = {'jsonify': False}
    return ap


class Base(DeclBase):
    '''Common functionality'''
    __abstract__ = True
    __json_null__ = True

    def __repr__(self):
        tpl = '{classname}:({name})'
        return tpl.format(classname=self.__class__.__name__, name=self.name)

    def __init__(self, name, **kwargs):
        self.name = name
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)

    def json(self):
        jsonify = lambda obj: obj.json() if hasattr(obj, 'json') else obj

        jsonout = {}

        for attr, prop in inspect(self.__class__).all_orm_descriptors.items():
            if hasattr(prop, 'info') and prop.info.get('jsonify'):
                value = getattr(self, attr)
                if self.__json_null__ or value is False or value:
                    if isinstance(value, (Sized, Iterable)) \
                        and not isinstance(value, basestring):
                        jsonout[attr] = [jsonify(p) for p in value]
                    else:
                        jsonout[attr] = jsonify(value)
        return jsonout


class Size(Base):
    '''Size classes'''
    __tablename__ = 'size'

    name = JSONColumn(String, primary_key=True, doc="Size name")
    space = JSONColumn(Float,
                       doc="length of side of square this size fills."
                       " e.g. 4 = 4x4")


class Language(Base):
    '''Languages'''
    __tablename__ = 'language'

    name = JSONColumn(String, primary_key=True, doc='Name of language')
    script = JSONColumn(String, doc='Script language is written in')


class BonusType(Base):
    '''Types of bonuses for effects. Affects stacking'''
    __tablename__ = 'bonustype'
    name = JSONColumn(String, primary_key=True, doc='Type of bonus')


class Dice(Base):
    '''Dice types'''
    __tablename__ = 'dice'

    name = JSONColumn(String, primary_key=True, doc='Dice name')
    sides = JSONColumn(Integer, nullable=False,
                       doc='Number of sides on the die')


class WeaponGroup(Base):
    '''Groups of Weapons'''
    __tablename__ = 'weapongroup'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of weapon group')


class WeaponProperty(Base):
    '''Properties Weapons may have'''
    __tablename__ = 'weaponproperty'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of weapon property')


class WeaponCategory(Base):
    '''Categories to which a weapon can belong'''
    __tablename__ = 'weaponcategory'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of weapon category')
    melee = JSONColumn(Boolean, default=False,
                       doc='Whether weapons in this category are melee')
    ranged = JSONColumn(Boolean, default=False,
                        doc='Whether weapons in this category are ranged')
    simple = JSONColumn(Boolean, default=False,
                        doc='Whether weapons in this category are simple')
    military = JSONColumn(
        Boolean, default=False,
        doc='Whether weapons in this category are military')
    superior = JSONColumn(
        Boolean, default=False,
        doc='Whether weapons in this category are superior')
    improvised = JSONColumn(
        Boolean, default=False,
        doc='Whether weapons in this category are improvised')


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

    name = JSONColumn(String, primary_key=True,
                      doc='Name of the weapon')
    proficiency_bonus = JSONColumn(
        Integer, default=+2, doc="Bonus to attack if character is proficient")
    dmg_mult = JSONColumn(
        Integer, default=1, doc='Number of dice to roll for damage')
    dicename = JSONColumn(
        String, ForeignKey('dice.name'), doc='Dice to roll for damage')
    groupname = JSONColumn(String,
                           ForeignKey('weapongroup.name'),
                           doc='Weapon group this weapon belongs to')
    categoryname = JSONColumn(String,
                              ForeignKey('weaponcategory.name'),
                              doc='Category this weapon belongs to')
    handedness = JSONColumn(Enum('One-Handed', 'Two-Handed'),
                            default='One-Handed',
                            doc='How many hands this weapon takes to wield')

    properties = jsonrelationship(WeaponProperty,
                                  secondary=weapon_weaponproperty,
                                  backref='weapons')


class ArmorType(Base):
    '''Types of armor'''
    __tablename__ = 'armortype'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of this armor type')
    weight = JSONColumn(
        Enum('Light', 'Heavy'), nullable=False,
        doc='The weight of this armor type (heavy or light)')


armor_effect = Table(
    'armor_effect',
    Base.metadata,
    Column('armorname', String, ForeignKey('armor.name'), primary_key=True),
    Column('effectname', String, ForeignKey('effect.name'), primary_key=True),
)


class Armor(Base):
    '''Represents a set of armor'''
    __tablename__ = 'armor'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of this set of armor')
    typename = JSONColumn(String, ForeignKey('armortype.name'), nullable=False,
                          doc='Type of armor this is')
    weight = JSONColumn(Integer, doc="This armor's weight in pounds.")

    effect = relationship('Effect', secondary='armor_effect', uselist=False)
    type = relationship(ArmorType, backref='armors')

    check = jsonassociation_proxy('effect', 'armor_check')
    ac_bonus = jsonassociation_proxy('effect', 'ac')
    speed = jsonassociation_proxy('effect', 'speed')

    def __init__(self, name, **kwargs):
        effect_attrs = {'check', 'ac_bonus', 'speed'}
        if effect_attrs & kwargs.viewkeys() and 'effect' not in kwargs:
            self.effect = Effect(name=name + "'s Effect")
        super(Armor, self).__init__(name, **kwargs)


class DamageType(Base):
    '''Damage types'''
    __tablename__ = 'damagetype'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of damage type')
    description = JSONColumn(
        String, doc='detailed description of the damage type')

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Alignment(Base):
    '''Alignments'''
    __tablename__ = 'alignment'

    name = JSONColumn(String, primary_key=True, doc="Alignment Name")
    good = JSONColumn(Boolean, default=False,
                  doc="Whether this alignment is good")
    evil = JSONColumn(Boolean, default=False,
                  doc="Whether this alignment is evil")
    lawful = JSONColumn(Boolean, default=False,
                    doc="Whether this alignment is lawful")
    chaotic = JSONColumn(Boolean, default=False,
                     doc="Whether this alignment is chaotic")


class Race(Base):
    '''Character race'''
    __tablename__ = 'race'

    name = JSONColumn(String, primary_key=True,
                      doc="Race's name")
    sizename = Column(String, ForeignKey('size.name'),
                      default='Medium',
                      doc="Race's size")
    effectname = Column(String, ForeignKey('effect.name'),
                        doc='Effect of being this race')

    size = jsonrelationship(Size)
    patron_deity = jsonrelationship('Deity',
                                    uselist=False,
                                    backref='patron_of_race')
    effect = jsonrelationship('Effect')

    def __init__(self, name, **kwargs):
        self.name = name
        if 'effect' in kwargs:
            self.effect = kwargs.pop('effect')
            self.effect.name = name + ' Racial Benefits'
            self.effect.bonustype_name = 'Racial'


class PowerSource(Base):
    '''A source of a class's power'''
    __tablename__ = 'powersource'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of the power source')
    description = JSONColumn(String, doc='Description of the power source')

    def __init__(self, name, description):
        self.name = name
        self.description = description


class_effect = Table(
    'class_effect',
    Base.metadata,
    Column('classname', String, ForeignKey('class.name'), primary_key=True),
    Column('effectname', String, ForeignKey('effect.name'), primary_key=True),
)


class Class(Base):
    '''Character classes'''
    __tablename__ = 'class'
    name = JSONColumn(String, primary_key=True, doc="Class name")
    powersource_name = JSONColumn(String, ForeignKey('powersource.name'),
                                  doc="Class's power source")
    role = JSONColumn(Enum('Leader',
                           'Controller',
                           'Striker',
                           'Defender'),
                      doc="Class's role in a party")
    effects = jsonrelationship('Effect', secondary=class_effect)

    def __init__(self, name, powersource_name, role, **kwargs):
        self.powersource_name = powersource_name
        self.role = role
        super(Class, self).__init__(name, **kwargs)


class DeityDomain(Base):
    '''Deity Domains'''
    __tablename__ = 'deity_domain'

    deityname = Column(String, ForeignKey('deity.name'),
                       doc='Deity this domain applies to')
    name = JSONColumn(String, primary_key=True, doc='Name of domain')


class Deity(Base):
    '''Deitys'''
    __tablename__ = 'deity'

    name = JSONColumn(String, primary_key=True, doc="Deity's name")
    alignmentname = JSONColumn(String, ForeignKey('alignment.name'),
                               doc="Deity's alignment")
    patron_of = JSONColumn(String, ForeignKey('race.name'),
                           doc='Race this Deity is a patron of')
    season = JSONColumn(Enum('Spring', 'Summer', 'Autumn', 'Winter'),
                        doc="Deity's season (if any)")

    domain_models = relationship(DeityDomain, backref='deity')
    domains = association_proxy('domain_models', 'name')
    alignment = relationship(Alignment)


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
    __json_null__ = False

    name = JSONColumn(String, primary_key=True, doc='Name of effect')
    bonustype_name = JSONColumn(String, ForeignKey('bonustype.name'),
                                doc='What kind of bonus type this counts as')
    max_hp = JSONColumn(Integer, doc="Mod to maximum hitpoints")
    intelligence = JSONColumn(Integer, doc="Mod to intelligence")
    constitution = JSONColumn(Integer, doc="Mod to constitution")
    dexterity = JSONColumn(Integer, doc="Mod to dexterity")
    wisdom = JSONColumn(Integer, doc="Mod to wisdom")
    charisma = JSONColumn(Integer, doc="Mod to charisma")
    strength = JSONColumn(Integer, doc="Mod to strength")
    initiative = JSONColumn(Integer, doc="Mod to initiative")
    fortitude = JSONColumn(Integer, doc="Mod to fortitude")
    will = JSONColumn(Integer, doc="Mod to will")
    reflex = JSONColumn(Integer, doc="Mod to reflex")
    armor_class = JSONColumn(Integer, doc="Mod to armor class")
    speed = JSONColumn(Integer, doc="Mod to speed")
    damage = JSONColumn(Integer, doc="Mod to damage")
    damage_mult = JSONColumn(Float, doc="Multiplier for damage")
    attack_roll = JSONColumn(Integer, doc="Mod to attack roll")
    saving_throw = JSONColumn(Integer, doc="Mod to saving throw roll")
    healing_surges = JSONColumn(Integer, doc="Mod to healing surges")
    vision = JSONColumn(Enum('Low-Light',
                             'Darkvision',
                             'Normal',
                             'Blind'),
                        doc="Change vision level to this")
    armor_check = Column(
        Integer, doc='Modifier to STR, DEX, and CON based '
                     'skill checks due to armor')

    stats = relationship('Stat', backref='effect')
    language_stats = relationship('LanguageStat')
    skill_stats = jsonrelationship('SkillStat')
    damage_stats = jsonrelationship('DamageStat')

    languages = jsonassociation_proxy('language_stats', 'language')

    def __init__(self, name=None, **kwargs):
        '''Allow the effect to be created unnamed. Will fail if trying to
        insert into db without naming it'''
        super(Effect, self).__init__(name, **kwargs)

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


class StatType(Base):
    '''Types of stats that can exist'''
    __tablename__ = 'stattype'
    name = Column(String, primary_key=True)


class Stat(Base):
    '''Multiple stats can be part of a single effect'''

    __tablename__ = 'stat'

    id = Column(Integer, primary_key=True, doc='Unique id of stat')
    effectname = Column(String, ForeignKey('effect.name'),
                        doc='Name of the effect this stat belongs to')
    stattype_name = Column(String,
                           ForeignKey('stattype.name'),
                           nullable=False,
                           doc='Kind of stat this is')
    __table_args__ = (Index('stat_effectname_idx', effectname),)
    __mapper_args__ = {'polymorphic_on': stattype_name}

    def __init__(self, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        #intentionally don't call super since we don't have a 'name'


class LanguageStat(Stat):
    '''Stat providing language comprehension'''
    __mapper_args__ = {'polymorphic_identity': 'Language'}

    language = JSONColumn(String, ForeignKey('language.name'),
                          doc="Language understanding bestowed")

    def __init__(self, language):
        self.language = language

    def __repr__(self):
        return 'Understands {}'.format(self.language)


class SkillStat(Stat):
    '''Stat modifying an skill'''
    __mapper_args__ = {'polymorphic_identity': 'Skill'}

    skillname = JSONColumn(String, ForeignKey('skill.name'),
                           doc="Name of skill modified")
    skill_mod = JSONColumn(Integer, doc='Mod to skill amount')

    def __init__(self, skillname, skill_mod):
        self.skillname = skillname
        self.skill_mod = skill_mod

    def __repr__(self):
        return '{0.skill_mod:+} {0.skillname}'.format(self)


class DamageStat(Stat):
    '''Stat modifying a damage type amount'''
    __mapper_args__ = {'polymorphic_identity': 'Damage'}

    damagetype_name = JSONColumn(
        String, ForeignKey('damagetype.name'),
        doc='Damage type resisted/weakened (null if any)')
    damagetype_mod = JSONColumn(Integer, doc='Mod to damage type')

    def __init__(self, damagetype_name, damagetype_mod):
        self.damagetype_name = damagetype_name
        self.damagetype_mod = damagetype_mod


class ProficiencyStat(Stat):
    '''Stat granting proficiency'''
    __mapper_args__ = {'polymorphic_identity': 'Proficiency'}

    weaponcategory_name = JSONColumn(
        String, ForeignKey('weaponcategory.name'),
        doc='name of weapon category proficiency granted')
    armortype_name = JSONColumn(
        String, ForeignKey('armortype.name'),
        doc='name of armor type proficiency granted')

    weaponcategory = relationship('WeaponCategory')
    armortype = relationship('ArmorType')

    @property
    def name(self):
        if self.weaponcategory_name is not None:
            return self.weaponcategory_name
        else:
            return self.armortype_name

    def __init__(self, cat, **kwargs):
        if isinstance(cat, WeaponCategory):
            self.weaponcategory_name = cat.name
        elif isinstance(cat, ArmorType):
            self.armortype_name = cat.name
        else:
            raise TypeError("Can't be proficient in {.name}".format(cat))
        super(ProficiencyStat, self).__init__(**kwargs)


class CharacterEncounter(Base):
    '''Links a player to an encounter in initiative order'''
    __tablename__ = 'character_encounter'

    charactername = JSONColumn(String, ForeignKey('character.name'),
                               primary_key=True,
                               doc='Character in initiative')
    encounter_id = Column(Integer, ForeignKey('encounter.name'),
                          primary_key=True,
                          doc='Encounter this init roll is for')
    init_score = JSONColumn(Integer,
                            doc='Initiative rolled for this encounter')
    position = Column(Integer, doc='Current position in the initiative order')
    second_wind_used = JSONColumn(Boolean, default=False,
                                  doc='Whether the character still has a '
                                  'second wind for this encounter.')

    character = relationship('Character', innerjoin=True, lazy='joined')


class Encounter(Base):
    '''Represents a single encounter'''
    __tablename__ = 'encounter'

    name = JSONColumn(String, primary_key=True, doc="Name of Encounter")
    sessionname = Column(String, ForeignKey('session.name'),
                         doc='Session this encounter belongs to')

    session = relationship('Session', backref='encounters')
    init_order = jsonrelationship('CharacterEncounter',
                                  order_by='CharacterEncounter.position',
                                  lazy='joined',
                                  collection_class=ordering_list('position'))
    players = jsonrelationship(
        'Character',
        secondary='character_encounter',
        secondaryjoin='and_('
        'CharacterEncounter.charactername == Character.name, '
        'Character.is_player)',
        order_by=Character.name)
    monsters = jsonrelationship(
        'Character',
        secondary='character_encounter',
        secondaryjoin='and_('
        'CharacterEncounter.charactername == Character.name, '
        '~Character.is_player'
        ')',
        order_by=Character.name)
    initiative = association_proxy('init_order', 'character')


class Session(Base):
    '''Play sessions'''
    __tablename__ = 'session'

    name = JSONColumn(String, primary_key=True,
                      doc='Name of this Session')
    date = JSONColumn(Date, doc="date session occurred on")
