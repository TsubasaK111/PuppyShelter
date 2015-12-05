from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, column_property

from sqlalchemy import (Table, Column, ForeignKey, Integer, String,
                        Date, DateTime, DefaultClause, func)
from sqlalchemy.sql import select

from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool


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


def puppy_before_insert(mapper, connection, targetPuppy):
    print "New puppy insert!"
    print "Mapper is:", mapper
    print "Connection is:", connection
    print "targetPuppy is:", targetPuppy

    #Count puppies in shelter, including this puppy that will be inserted.
    shelter_count = connection.execute("""SELECT COUNT(*)
                                          FROM puppy
                                          WHERE shelter_id == ?
                                       """,
                                       (targetPuppy.shelter_id,)
                                       ).scalar() + 1
    print "shelter_count is: ", shelter_count

    #calculating remaining space
    remaining_capacity = connection.execute("""
            SELECT (maximum_capacity - ?) AS r
            FROM shelter
            WHERE id == ?
        """,
        (shelter_count, targetPuppy.shelter_id,)
        ).scalar()
    print "remaining capacity is:", remaining_capacity

    if remaining_capacity < 0:
        print "this shelter is full! Try another shelter :("

    else:
        occupancy_update_result = connection.execute("""
                UPDATE shelter
                SET current_occupancy = ?
                WHERE id = ?
            """,
            (shelter_count, targetPuppy.shelter_id,)
            )
        print targetPuppy.name, " has been put into: ", occupancy_update_result

listen(Puppy, 'before_insert', puppy_before_insert)

def recieve_before_flush(session, flush_context, instances):
    """listen for the 'before_flush' event"""
    print "Session is: ", session
    print "Session.new is: ", session.new
    showShelter = session.execute("SELECT * FROM shelter").fetchall()
    # session.execute(
    #         shelter.update().\
    #             values(current_occupancy = puppies_in_this_shelter(self)).\
    #             where(shelter.id == self.shelter_id)
    #
    #     select([func.count(Puppy.id)]).where(Puppy.id == ).limit(1)
    # ).fetchall()
    print showShelter

listen(session, 'before_flush', recieve_before_flush)
