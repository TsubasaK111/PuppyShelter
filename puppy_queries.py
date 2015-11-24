from datetime import date
from sqlalchemy import Date
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import functions
from puppy_setup import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyShelters.db', echo = True)

Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()

# 1. Query all of the puppies and return the results in ascending alphabetical order
def alphabeticalPuppies():
    puppies = session.query(Puppy).order_by(Puppy.name.desc())
    for puppy in puppies:
        print puppy.name

    tisToday = str(date.today())


# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
def youngPups():
    puppies = session.query(Puppy).filter(Puppy.dateOfBirth > func.date(date.today())).order_by(Puppy.dateOfBirth.desc())

    for puppy in puppies:
        print puppy.name
        print puppy.dateOfBirth

    # print date.today()
    # print functions.current_date()


# 3. Query all puppies by ascending weight
def weightedPuppies():
    """ """

# 4. Query all puppies grouped by the shelter in which they are staying
def shelteredPuppies():
    """ """

def runAll():
    alphabeticalPuppies()
    youngPups()
    weightedPuppies()
    shelteredPuppies()
    print "Success!  All queries run!"

if __name__ == '__main__':
    runAll()
