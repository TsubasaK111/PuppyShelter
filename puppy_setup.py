from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

from sqlalchemy import (Table, Column, ForeignKey, Integer, String,
                        Date, DateTime, DefaultClause, func)
from sqlalchemy.sql import select

from sqlalchemy.event import listen
from sqlalchemy.pool import Pool

Base = declarative_base()

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
    current_occupancy = Column( Integer )
    id = Column(Integer, primary_key = True)

    # Many to many relationship with Puppy.
    # Puppies can be adopted by one person, or a family of people.
    # Similarly, a person or family can adopt one or several puppies.
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

    # current_occupancy_count = select([func.count(puppy.id)]).\
    #                           where(puppy.id == self.id).\
    #                           limit(1)
    # def current_occupancy_counter(self):
    #     shelter.update().\
    #     where(shelter.id == self.shelter_id).\
    #     values(current_occupancy = current_occupancy_count)
    # current_occupancy_counter()

    # One to one relationship with Puppy_Profile
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
    id = Column( Integer, primary_key = True )


engine = create_engine('sqlite:///puppyShelters.db', echo = True)


Base.metadata.create_all(engine)


def my_on_connect(dbapi_con, connection_record):
    print "New DBAPI connection:", dbapi_con

def puppy_connect(dbapi_con, connection_record):
    print "New puppy connection:", dbapi_con

def puppy_insert(mapper, connection, target):
    print "New puppy insert!"
    print "Mapper is:", mapper
    print "Connection is:", connection
    print "Target is:", target
    print "Target name is:", target.name
    current_occupancy_count = select([func.count(Puppy.id)]).\
                              where(Puppy.shelter_id == target.shelter_id).\
                              limit(1)
    print current_occupancy_count
    current_occupancy_counter = shelter.update().\
                                where(Shelter.id == target.shelter_id).\
                                values(current_occupancy = current_occupancy_count)
    print current_occupancy_counter
    # connection.execute(current_occupancy_counter)

    # print current_occupancy_counter
listen(Pool, 'connect', my_on_connect)

listen(Puppy, 'after_insert', puppy_insert)
