from sqlalchemy import text, func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies.models import Base, Shelter, Puppy


engine = create_engine('sqlite:///puppyShelters.db')


Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()


def alphabeticalPuppies():
    """1. Query puppies and return results in ascending alphabetical order"""

    print "\n Puppies in alphabetical order:"

    puppies = session.query(Puppy).order_by(Puppy.name.asc())
    for puppy in puppies:
        print puppy.name


def youngPups():
    """2. Query all puppies less than 6 months old ordered by youngest first"""

    print "\n Puppies less than 6 months old:"

    youngPuppies = session.query(Puppy).from_statement(text("""
        SELECT * FROM Puppy
        WHERE( julianday(dateOfBirth) > (julianday('now') -183) )
        ORDER BY dateOfBirth
    """))
    for puppy in youngPuppies:
        print puppy.name, puppy.dateOfBirth


def weightedPuppies():
    """3. Query all puppies by ascending weight"""

    print "\n Puppies in weight order:"

    puppies = session.query(Puppy).order_by(Puppy.weight)
    for puppy in puppies:
        print puppy.name, puppy.weight


def shelteredPuppies():
    """4. Query all puppies grouped by the shelter in which they are staying"""

    print "\n Puppies grouped by shelter:"

    for thisShelter in session.query(Shelter).\
                               join(Puppy).\
                               filter(Shelter.id == Puppy.shelter_id).\
                               group_by(Shelter.id):
        print " \n" + str(thisShelter.name) + " :"
        for thisPuppy in session.query(Puppy).\
                                 filter(Puppy.shelter_id == thisShelter.id).\
                                 order_by(Puppy.name):
            print thisPuppy.name


def runAll():
    alphabeticalPuppies()
    youngPups()
    weightedPuppies()
    shelteredPuppies()
    print "Success!  All queries run!"


if __name__ == '__main__':
    runAll()
