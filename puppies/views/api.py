from flask import render_template, url_for, request, redirect, flash, jsonify

from puppies import app
from puppies.models import session, Shelter, Puppy, Puppy_Profile, Adopter
from puppies.forms import *

import pdb, pprint

#GET Req API endpoint
@app.route('/shelters/<int:shelter_id>/menu/<int:puppy_id>/JSON/')
def puppyJSON(shelter_id, puppy_id):
    shelter = session.query(Shelter).filter_by(id = shelter_id).one()
    puppy = session.query(Puppy).filter_by(shelter_id = shelter_id).filter_by(id = puppy_id).one()
    return jsonify(Puppy = puppy.serialize)


#GET Req API endpoint
@app.route('/shelters/<int:shelter_id>/menu/JSON/')
def show_puppies_JSON(shelter_id):
    shelter = session.query(Shelter).filter_by(id = shelter_id).one()
    puppies = session.query(Puppy).filter_by(shelter_id = shelter_id).all()
    return jsonify(Puppies = [puppy.serialize for puppy in puppies])
