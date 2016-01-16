from flask import render_template, url_for, request, redirect, flash, jsonify

from puppies import app
from puppies.models import session, Shelter, Puppy, Puppy_Profile, Adopter
from puppies.forms import *

from decimal import *

import pprint, pdb, logging

logger = logging.getLogger(__name__)


@app.route('/adopters/')
def show_adopters():
    output = render_template( 'page_head.html',
                              title = "California State Puppy Adopter Directory",
                              form = 0 )
    adopters = session.query(Adopter).all()
    output += render_template('show_adopters.html', adopters=adopters)
    return output


@app.route('/adopters/new/', methods=['GET', 'POST'])
def new_adopter():
    """page to create a new adopter."""
    form = AdopterForm(request.form)
    if request.method == "POST":
        new_adopter = Adopter()
        form.populate_obj(new_adopter)
        session.add(new_adopter)
        session.commit()
        flash( "New adopter '" + new_adopter.name + "' added!")
        return redirect(url_for("show_adopters"))

    else:
        output = render_template(
            'page_head.html',
            title = "Add a New Adopter! XD",
            form = form )
        output += render_template('new_adopter.html', form = form )
        return output


@app.route('/adopters/<int:adopter_id>/edit/', methods=['GET', 'POST'])
def edit_adopter(adopter_id):
    """page to edit a adopter's basic information."""
    adopter = session.query(Adopter).filter_by(id=adopter_id).first()
    form = AdopterForm( request.form, adopter )
    if request.method == "POST":
        old_name = adopter.name
        form.populate_obj(adopter)
        session.add(adopter)
        session.commit()
        flash( "Adopter '"+old_name+"' renamed to '"+adopter.name+"'. Jawohl!")
        return redirect(url_for("show_adopters"))

    else:
        output = render_template( 'page_head.html',
                                  title = "Edit an Adopter",
                                  form = form )
        output += render_template( 'edit_adopter.html',
                                   form = form )
        return output


@app.route('/adopters/<int:adopter_id>/delete/', methods=["GET","POST"])
def delete_adopter(adopter_id):
    """page to delete a puppy."""
    adopter = session.query(Adopter).filter_by(id=adopter_id).first()
    form = AdopterForm( request.form, adopter )
    if request.method == "POST":
        session.delete(adopter)
        session.commit()
        flash( "Adopter '" + adopter.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("show_adopters"))

    else:
        output = render_template( 'page_head.html',
                                  title = "Delete an Adopter",
                                  form = form )
        output += render_template( 'delete_adopter.html',
                                   form = form )
        return output
