import sys
from sqlalchemy import column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite:///puppyshelters.db')
Base.metadata.create_all(engine)

class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column( String(50), nullable = False )
    address = Column( String(200) )
    city = Column( String(50) )
    state = Column( String(50) )
    zipCode = Column( Integer )
    website = Column( URL )
    id = Column(Integer, primary_key = True)
class Puppy(Base):
    __tablename__= 'puppy'
    name = Column( String(50), nullable = False )
    'date of birth' = Column( Date )
    gender = Column( String(14) )
    weight = Column( Decimal )
    shelter_id = ( Integer, ForeignKey('shelter.id') )
