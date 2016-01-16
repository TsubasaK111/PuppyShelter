from flask import render_template, url_for, request, redirect, flash, jsonify

from puppies import app
from puppies.models import session, Shelter, Puppy, Puppy_Profile, Adopter
from puppies.forms import *

from decimal import *

import pprint, pdb, logging

logger = logging.getLogger(__name__)


@app.route('/shelters/')
def show_shelters():
    output = render_template( 'page_head.html',
                              title = "California State Puppy Shelters",
                              form = 0 )
    shelters = session.query(Shelter).all()
    output += render_template('show_shelters.html', shelters=shelters)
    return output


@app.route('/shelters/new/', methods=['GET', 'POST'])
def new_shelter():
    """page to create a new shelter."""
    form = ShelterForm(request.form)
    if request.method == "POST" and form.validate():
        new_shelter = Shelter()
        form.populate_obj(new_shelter)
        session.add(new_shelter)
        session.commit()
        flash( "New shelter '" + new_shelter.name + "' added!")
        return redirect( url_for("show_shelters") )

    else:
        output = render_template(
            'page_head.html',
            title = "Add a new shelter to the great state of California!",
            form = form )
        output += render_template( 'new_shelter.html', form = form )
        return output


@app.route('/shelters/<int:shelter_id>/edit/', methods=['GET', 'POST'])
def edit_shelter(shelter_id):
    """page to edit a shelter's basic information."""
    shelter = session.query(Shelter).filter_by(id=shelter_id).first()
    form = ShelterForm( request.form, shelter )
    if request.method == "POST":
        old_name = shelter.name
        form.populate_obj(shelter)
        session.add(shelter)
        session.commit()
        flash( "Shelter '"+old_name+"' renamed to '"+shelter.name+"'. Jawohl!")
        return redirect(url_for("show_shelters"))

    else:
        output = render_template( 'page_head.html',
                                  title = "Rename Your Shelter",
                                  form = form )
        output += render_template( 'edit_shelter.html',
                                   form = form )
        return output


@app.route('/shelters/<int:shelter_id>/delete/', methods=["GET","POST"])
def delete_shelter(shelter_id):
    """page to delete a puppy."""
    shelter = session.query(Shelter).filter_by(id=shelter_id).first()
    form = ShelterForm( request.form, shelter )
    if request.method == "POST":
        session.delete(shelter)
        session.commit()
        flash( "Shelter '" + shelter.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("show_shelters"))

    else:
        output = render_template( 'page_head.html',
                                  title = "Delete a Shelter",
                                  form = form )
        output += render_template( 'delete_shelter.html',
                                   form = form )
        return output
