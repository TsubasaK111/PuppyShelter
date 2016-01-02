from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppy_db_setup import Base, Shelter, Puppy, Puppy_Profile, Adopter

import pdb
import pprint


import puppies.views

app = Flask(__name__)


engine = create_engine('sqlite:///puppyShelters.db')
Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()


if __name__ == "__main__":
    app.secret_key = "ZUPA_SECRET_KEY!!!"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5001)
