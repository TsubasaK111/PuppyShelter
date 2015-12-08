from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, column_property

from sqlalchemy import (Table, Column, ForeignKey, Integer, String,
                        Date, DateTime, DefaultClause, func)
from sqlalchemy.sql import select, text

from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

import pprint
import pdb


Base = declarative_base()


# Declare table for many to many relationship with Puppy_Profile
association_table = Table('association', Base.metadata,
    Column('shelter_id', Integer, ForeignKey('shelter.id')),
    Column('puppy_id', Integer, ForeignKey('puppy.id'))
)


class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column( String(50), nullable = False )
    address = Column( String(200) )
    city = Column( String(50) )
    state = Column( String(50) )
    zipCode = Column( Integer )
    website = Column( String )
    maximum_capacity = Column( Integer )
    id = Column(Integer, primary_key = True)
    current_occupancy = Column( Integer )

    # Declare many to many relationship with Puppy_Profile
    puppies = relationship(
        "Puppy",
        secondary = association_table,
        backref="shelters"
    )


class Puppy(Base):
    __tablename__ = 'puppy'
    name = Column( String(50), nullable = False )
    dateOfBirth = Column( Date )
    gender = Column( String(14) )
    weight = Column( String(14) )
    entry_date = Column( DateTime, default=func.now() )
    shelter_id = Column( Integer, ForeignKey('shelter.id') )
    id = Column( Integer, primary_key = True )

    # Declare one to one relationship with Puppy_Profile
    puppy_profile = relationship(
        "Puppy_Profile",
        uselist=False,
        backref="puppy"
    )


class Puppy_Profile(Base):
    __tablename__ = 'puppy_profile'
    puppy_id = Column( Integer, ForeignKey('puppy.id') )
    picture = Column(String)
    description = Column( String(500) )
    special_needs = Column( String(200) )
    hair_length = Column( String(14) )
    number_of_tricks = Column( String(14) )
    id = Column( Integer, primary_key = True )


# engine = create_engine('sqlite:///puppyShelters.db', echo = True)
engine = create_engine('sqlite:///puppyShelters.db')


Base.metadata.create_all(engine)


Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)


session = DBSession()


puppies_on_hold = []


def occupancy_reporter(session,this_shelter_id):
    print "placeholder"


def after_attach(session, instance):
    print "\nnew attach!!\n"
    print "instance is: ", instance
    print "Session.new is: ", session.new
    if instance.__tablename__ == "shelter":
        print "it's a shelter attach!"
        print instance
        session.flush()


event.listen(session, 'after_attach', after_attach)


def before_flush(session, flush_context, instances):
    print "\nnew flush!!\n"
    print "Session.new is: ", session.new
    for each in session.new:
        print each.__tablename__
        if each.__tablename__ == "puppy":

            #extract shelter_id
            print "each.shelter_id is: ", each.shelter_id

            #calculate number of puppies in shelter if this puppy is added.
            shelter_count_SQL = text("""
                                SELECT COUNT(*)
                                FROM puppy
                                WHERE shelter_id =:shelter_id """)
            shelter_count = session.execute(
                    shelter_count_SQL,
                    {"shelter_id": each.shelter_id}
                ).scalar() + 1
            print "shelter_count is: ", shelter_count

            #calculating remaining space
            remaining_capacity_SQL = text("""
                                SELECT (maximum_capacity - :shelter_count) AS r
                                FROM shelter
                                WHERE id =:shelter_id""")
            remaining_capacity = session.execute(
                    remaining_capacity_SQL,
                    {"shelter_count": shelter_count,
                    "shelter_id": each.shelter_id}
                ).scalar()
            print "remaining capacity is:", remaining_capacity

            if remaining_capacity < 0:
                print "shelter is full! We're gonna have to kill yo doggie :("
                puppies_on_hold.append(each)
                print puppies_on_hold
                session.expunge(each)
                print "doggie sent to heaven!"
                pdb.set_trace()
            else:
                occupancy_update_result = session.execute("""
                        UPDATE shelter
                        SET current_occupancy = :shelter_count
                        WHERE id = :shelter_id
                    """,
                    {"shelter_count": shelter_count, "shelter_id": each.shelter_id}
                    )
                print each.name, " has been put into: ", occupancy_update_result
                print "shelter_count updated!"


event.listen(session, 'before_flush', before_flush)
