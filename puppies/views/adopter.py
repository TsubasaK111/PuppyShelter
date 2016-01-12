from flask import render_template, url_for, request, redirect, flash, jsonify

from puppies import app

from puppies.models import session, Shelter, Puppy, Puppy_Profile, Adopter

from puppies.forms import *

from decimal import *

import pdb, pprint


###############
#adopters CRUD
###############

@app.route('/adopters/')
def show_adopters():
    output = render_template( 'page_head.html',
                              title = "California State Puppy Adopter Directory",
                              form = 0 )
    adopters = session.query(Adopter).all()
    output += render_template('show_adopters.html')
    return output


@app.route('/adopters/<int:adopter_id>/')
def show_puppies_by_adopter(adopter_id):
    adopter = session.query(Adopter).filter_by(id = adopter_id).first()
    puppies = session.query(Puppy).filter_by(adopter_id = adopter_id)

    output = render_template( 'page_head.html',
                              title = "The Puppies of "+adopter.name,
                              form = 0 )
    output += render_template( 'show_puppies_by_adopter.html',
                               adopter=adopter,
                               puppies=puppies )
    return output


@app.route('/adopters/<int:adopter_id>/adopt/', methods=['GET', 'POST'])
def adopt_puppy(adopter_id):
    """page to adopt puppies, accessed from the Adopter directory."""

    if request.method == "POST":
        adopt_this_puppy_id = request.form["adopt_this_puppy_id"]
        adopt_this_puppy_name = session.query(Puppy).\
                                filter_by(id = adopt_this_puppy_id).first().name
        result = session.execute("""
            UPDATE puppy
            SET adopter_id = :adopter_id,
                shelter_id = NULL
            WHERE id = :adopt_this_puppy_id
        """,
        { "adopter_id": adopter_id,
          "adopt_this_puppy_id": adopt_this_puppy_id }
        )
        session.commit()
        flash("Puppy '" + adopt_this_puppy_name + "' adopted! Congrats!")
        return redirect(url_for("adopt_puppy", adopter_id = adopter_id))

    if request.method == "GET":
        output = render_template('page_head.html', title = "Adopt a Puppy!!!", form = 0)
        adopter = session.query(Adopter).filter_by(id = adopter_id).first()
        puppies = session.execute("""
                SELECT *
                FROM puppy
                WHERE adopter_id ISNULL
            """)
        # print "puppies length is: ", len(puppies)
        flash("Please select a puppy to adopt.")
        output += render_template( 'adopt_puppy.html',
                                   adopter=adopter,
                                   puppies=puppies )
        return output


@app.route('/adopters/new/', methods=['GET', 'POST'])
def new_adopter():
    """page to create a new menu item."""
    if request.method == "POST":
        new_name = request.form['new_name']
        new_adopter = Adopter( name=new_name )
        session.add(new_adopter)
        session.commit()
        # flash( "New adopter '" + new_name + "' added!")
        return redirect(url_for("show_adopters"))

    else:
        output = render_template('page_head.html', title = "Add a New Adopter! XD", form = 0)
        # output += "new_adopter!!"
        output += render_template('new_adopter.html')
        return output


@app.route('/adopters/<int:adopter_id>/edit/', methods=['GET', 'POST'])
def edit_adopter(adopter_id):
    """page to edit a adopter's basic information."""
    if request.method == "POST":
        edited_name = request.form['edited_name']
        old_name = session.query(Adopter).filter_by(id=adopter_id).first().name
        result = session.execute("""
                UPDATE adopter
                SET name=:edited_name
                WHERE id=:edited_adopter_id;
            """,
            {"edited_name": edited_name,
            "edited_adopter_id": adopter_id}
        )
        session.commit()
        flash( "Adopter '"+old_name+"' renamed to '"+edited_name+"'. Jawohl!")
        return redirect(url_for("show_adopters"))

    else:
        output = render_template('page_head.html', title = "Edit a Adopter", form = 0)
        adopter = session.query(Adopter).filter_by(id = adopter_id).first()
        output += render_template('edit_adopter.html', adopter = adopter )
        return output


@app.route('/adopters/<int:adopter_id>/delete/', methods=["GET","POST"])
def delete_adopter(adopter_id):
    """page to delete a puppy."""
    if request.method == "POST":
        delete_this_adopter = session.query(Adopter).filter_by(id = adopter_id).first()
        session.delete(delete_this_adopter)
        session.commit()
        flash( "Adopter '" + delete_this_adopter.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("show_adopters"))

    else:
        output = render_template('page_head.html', title = "Delete an Adopter", form = 0)
        adopter = session.query(Adopter).filter_by(id = adopter_id).first()
        output += render_template( 'delete_adopter.html', adopter = adopter )
        return output
