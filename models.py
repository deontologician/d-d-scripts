from sqlalchemy import (Column, Integer, String, Float, ForeignKey, Boolean,
                        Enum)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

DeclBase = declarative_base()


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

    def __init__(self, name, power_source, role):
        self.name = name
        self.power_source = power_source
        self.role = role


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
    __tablename__ = 'player'

    name = Column(String, primary_key=True, doc="Character's name")
    racename = Column(String, ForeignKey('race.name'), default='Human',
                      doc="Character's race")
    classname = Column(String, ForeignKey('class.name'),
                       doc="Character's class")
    height = Column(String,
                    doc="Character's height")
    weight = Column(Integer,
                    doc="Character's weight (in lbs)")
    gender = Column(String,
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

    misc_init = Column(Integer, default=0)

    # Relationships
    deity = relationship(Deity)
    class_ = relationship(Class)
    alignment = relationship(Alignment)
    race = relationship(Race)
