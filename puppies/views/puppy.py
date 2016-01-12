from flask import render_template, url_for, request, redirect, flash, jsonify

from puppies import app

from puppies.models import session, Shelter, Puppy, Puppy_Profile, Adopter

from puppies.forms import *

from decimal import *

import pdb, pprint


###############
#puppies CRUD
###############

@app.route('/shelters/<int:shelter_id>/')
def show_puppies(shelter_id):
    shelter = session.query(Shelter).filter_by(id = shelter_id).first()
    puppies = session.query(Puppy).filter_by(shelter_id = shelter_id)
    # pdb.set_trace()
    output = render_template( 'page_head.html',
                              title = "The Puppies of "+shelter.name,
                              form = 0 )
    output += render_template( 'show_puppies.html',
                               shelter=shelter,
                               puppies=puppies )
    return output


@app.route('/shelters/<int:shelter_id>/new/', methods=['GET', 'POST'])
def new_puppy(shelter_id):
    """page to create a new menu item."""
    form = NewPuppyForm(request.form)
    if request.method == "POST" and form.validate():
        new_name = request.form['name']
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        if (shelter.maximum_capacity - shelter.current_occupancy) <= 0:
            flash( """
                '{shelter_name}' is full, and the puppy
                '{new_name}' couldn't be added, sorry :(
                """.format(shelter_name=shelter.name, new_name=new_name))
            return redirect(url_for("show_puppies", shelter_id=shelter.id))
        else:
            new_puppy = Puppy( name=new_name )
            form.populate_obj(new_puppy)
            session.add(new_puppy)
            session.commit()
            flash( "new puppy '" + new_name + "' added!")
            return redirect(url_for("show_puppies", shelter_id=shelter.id))

    else:
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output = render_template('page_head.html', title = "Add a New Puppy! :D", form = 0)
        output += render_template( 'new_puppy.html',
                                   shelter = shelter,
                                   form = form )
        return output


@app.route('/shelters/<shelter_id>/<int:puppy_id>/edit/', methods=['GET', 'POST'])
def edit_puppy(shelter_id, puppy_id):
    """page to edit a puppy's basic information."""
    if request.method == "POST":
        edited_name = request.form['edited_name']
        old_name = session.query(Puppy).filter_by(id = puppy_id).first().name

        result = session.execute("""
                UPDATE puppy
                SET name=:edited_name
                WHERE id=:edited_puppy_id;
            """,
            {"edited_name": edited_name,
            "edited_puppy_id": puppy_id}
        )
        session.commit()
        flash( "item '" +  old_name + "' edited to '" + edited_name + "'. Jawohl!")
        return redirect(url_for("show_puppies", shelter_id=shelter_id))

    else:
        output = render_template('page_head.html', title = "The Menu Manager", form = 0)
        puppy = session.query(Puppy).filter_by(id = puppy_id).first()
        print "shelter_id is: ", shelter_id
        if shelter_id == "n":
            shelter = session.query(Shelter).filter_by(id = puppy.shelter_id).first()
        else:
            shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output += render_template('edit_puppy.html',
                                  shelter = shelter,
                                  puppy = puppy )
        return output


@app.route('/shelters/<shelter_id>/<int:puppy_id>/delete/', methods=["GET","POST"])
def delete_puppy(shelter_id, puppy_id):
    """page to delete a puppy."""
    if request.method == "POST":
        delete_this_puppy = session.query(Puppy).filter_by(id = puppy_id).first()
        session.delete(delete_this_puppy)
        session.commit()
        flash( "item '" + delete_this_puppy.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("show_puppies", shelter_id=shelter_id))

    else:
        output = render_template('page_head.html', title = "The Menu Manager", form = 0)
        puppy = session.query(Puppy).filter_by(id = puppy_id).first()
        if shelter_id == "n":
            shelter = session.query(Shelter).filter_by(id = puppy.shelter_id).first()
        else:
            shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output += render_template( 'delete_puppy.html',
                                   puppy = puppy,
                                   shelter = shelter )
        return output
