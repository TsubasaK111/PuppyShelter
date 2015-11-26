from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column( String(50), nullable = False )
    address = Column( String(200) )
    city = Column( String(50) )
    state = Column( String(50) )
    zipCode = Column( Integer )
    website = Column( String(100) )
    id = Column(Integer, primary_key = True)
class Puppy(Base):
    __tablename__= 'puppy'
    name = Column( String(50), nullable = False )
    dateOfBirth = Column( Date )
    gender = Column( String(14) )
    weight = Column( String(14) )
    picture = Column(String)
    shelter_id = Column( Integer, ForeignKey('shelter.id') )
    id = Column( Integer, primary_key = True )

engine = create_engine('sqlite:///puppyShelters.db')
Base.metadata.create_all(engine)
