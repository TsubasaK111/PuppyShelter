from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, column_property

from sqlalchemy import (Table, Column, ForeignKey, Integer, String,
                        Boolean, Date, DateTime, DefaultClause, func)
from sqlalchemy.sql import select, text

from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

import pprint
import pdb


Base = declarative_base()


# Table for many to many relationship with Puppy
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

    # Many to many relationship with Puppy
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
    adopter_id = Column( Integer, ForeignKey('adopter.id') )
    id = Column( Integer, primary_key = True )

    # One to one relationship with Puppy_Profile
    puppy_profile = relationship(
        "Puppy_Profile",
        uselist=False,
        backref="puppy"
    )

    # Declare many to one relationship with Adopter
    adopter = relationship( "Adopter" )


class Puppy_Profile(Base):
    __tablename__ = 'puppy_profile'
    puppy_id = Column( Integer, ForeignKey('puppy.id') )
    picture = Column(String)
    description = Column( String(500) )
    special_needs = Column( String(200) )
    hair_length = Column( String(14) )
    number_of_tricks = Column( String(14) )
    id = Column( Integer, primary_key = True )

class Adopter(Base):
    __tablename__ = 'adopter'
    name = Column( String(50), nullable = False )
    address = Column( String(200) )
    city = Column( String(50) )
    state = Column( String(50) )
    zipCode = Column( Integer )
    entry_date = Column( DateTime, default=func.now() )
    adoption_date = Column( Date )
    id = Column ( Integer, primary_key = True )

# engine = create_engine('sqlite:///puppyShelters.db', echo = True)
engine = create_engine('sqlite:///puppyShelters.db')


Base.metadata.create_all(engine)


Base.metadata.bind = engine


DatabaseSession = sessionmaker(bind=engine)


session = DatabaseSession()


puppies_on_hold = []


#calculate number of puppies in shelter.
def current_occupancy_counter(session, this_shelter_id):
    puppy_count_SQL = text("""
                        SELECT COUNT(*)
                        FROM puppy
                        WHERE shelter_id =:this_shelter_id AND adopter_id ISNULL
                        """)
    puppy_count = session.execute(
            puppy_count_SQL,
            {"this_shelter_id": this_shelter_id}
        ).scalar()
    print "puppy_count is: ", puppy_count
    return puppy_count

def remaining_capacity_counter(session, this_shelter_id):
    current_occupancy = current_occupancy_counter(session, this_shelter_id)
    remaining_capacity_SQL = text("""
                        SELECT (maximum_capacity - :current_occupancy) AS r
                        FROM shelter
                        WHERE id =:shelter_id""")
    remaining_capacity = session.execute(
            remaining_capacity_SQL,
            {"current_occupancy": current_occupancy,
            "shelter_id": this_shelter_id}
        ).scalar()
    print "remaining capacity is:", remaining_capacity
    return remaining_capacity, current_occupancy

def load_balancer(session, this_puppy_id):
    remaining_capacity_list = []
    shelters = session.query(Shelter).order_by(Shelter.id.asc())
    for shelter in shelters:
        remaining_capacity, ignore = remaining_capacity_counter(session, shelter.id)
        remaining_capacity_list.append(remaining_capacity)
    print remaining_capacity_list
    print remaining_capacity_list.index(max(remaining_capacity_list))

def adopt_puppy(session, puppy_id, adopter_id):
    update_puppy_SQL = text("""
                        UPDATE puppy
                        SET adopter_id = :adopter_id,
                            shelter_id = NULL
                        WHERE id = :puppy_id""")
    update_puppy_result = session.execute(
                                      update_puppy_SQL,
                                      {"puppy_id": puppy_id,
                                      "adopter_id": adopter_id}
                                         )
    print "update_puppy_result: ", update_puppy_result

def after_attach(session, instance):
    """ flush session (commit all changes to the SQL db)
        whenever a 'shelter' is added. """
    print "\nnew attach! instance is: ", instance
    print "Session.new is: ", session.new
    if instance.__tablename__ == "shelter":
        session.flush()


event.listen(session, 'after_attach', after_attach)


def before_flush(session, flush_context, instances):
    """populate the "current_occupancy" column, prevent puppy overflows."""
    print "\nnew flush! Session.new is: ", session.new
    for each in session.new:
        print "__tablename__ is: ", each.__tablename__
        if each.__tablename__ == "puppy":
            print "each.shelter_id is: ", each.shelter_id
            remaining_capacity, current_occupancy = remaining_capacity_counter(
                                                            session,
                                                            each.shelter_id)
            if remaining_capacity - 1 < 0:
                puppies_on_hold.append(each)
                print "shelter full! puppies_on_hold: ", puppies_on_hold
                session.expunge(each)
                pdb.set_trace()
            else:
                occupancy_update_result = session.execute("""
                        UPDATE shelter
                        SET current_occupancy = :current_occupancy
                        WHERE id = :shelter_id
                    """,
                    {"current_occupancy": current_occupancy,
                    "shelter_id": each.shelter_id}
                    )
                print each.name, " has been put into: ", occupancy_update_result


event.listen(session, 'before_flush', before_flush)
