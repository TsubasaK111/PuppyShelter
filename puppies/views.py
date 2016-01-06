from flask import render_template, url_for, request, redirect, flash, jsonify

from puppies import app

from models import session, Shelter, Puppy, Puppy_Profile, Adopter

from forms import NewPuppyForm

###############
#shelters CRUD
###############


@app.route('/shelters/')
def show_shelters():
    output = render_template('page_head.html', title = "The State Shelter Manager")
    shelters = session.query(Shelter).all()
    output += render_template('show_shelters.html', shelters=shelters)
    return output

@app.route('/shelters/new/', methods=['GET', 'POST'])
def new_shelter():
    """page to create a new menu item."""
    if request.method == "POST":
        new_name = request.form['new_name']
        new_shelter = Shelter( name=new_name )
        session.add(new_shelter)
        session.commit()
        flash( "New shelter '" + new_name + "' added!")
        return redirect(url_for("show_shelters"))

    else:
        output = render_template('page_head.html', title = "Add a New Shelter! XD")
        # output += "new_shelter!!"
        output += render_template('new_shelter.html')
        return output


@app.route('/shelters/<int:shelter_id>/edit/', methods=['GET', 'POST'])
def edit_shelter(shelter_id):
    """page to edit a shelter's basic information."""
    if request.method == "POST":
        edited_name = request.form['edited_name']
        old_name = session.query(Shelter).filter_by(id=shelter_id).first().name
        result = session.execute("""
                UPDATE shelter
                SET name=:edited_name
                WHERE id=:edited_shelter_id;
            """,
            {"edited_name": edited_name,
            "edited_shelter_id": shelter_id}
        )
        session.commit()
        flash( "Shelter '"+old_name+"' renamed to '"+edited_name+"'. Jawohl!")
        return redirect(url_for("show_shelters"))

    else:
        output = render_template('page_head.html', title = "Edit a Shelter")
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output += render_template('edit_shelter.html', shelter = shelter )
        return output


@app.route('/shelters/<int:shelter_id>/delete/', methods=["GET","POST"])
def delete_shelter(shelter_id):
    """page to delete a puppy."""
    if request.method == "POST":
        delete_this_shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        session.delete(delete_this_shelter)
        session.commit()
        flash( "Shelter '" + delete_this_shelter.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("show_shelters"))

    else:
        output = render_template('page_head.html', title = "Delete a Shelter")
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output += render_template( 'delete_shelter.html', shelter = shelter )
        return output


###############
#puppies CRUD
###############

@app.route('/shelters/<int:shelter_id>/')
def show_puppies(shelter_id):
    output = render_template('page_head.html', title = "The Puppy Manager")
    shelter = session.query(Shelter).filter_by(id = shelter_id).first()
    puppies = session.query(Puppy).filter_by(shelter_id = shelter_id)
    output += render_template( 'show_puppies.html',
                               shelter=shelter,
                               puppies=puppies )
    return output

@app.route('/adopters/<int:adopter_id>/')
def show_puppies_by_adopter(adopter_id):
    output = render_template('page_head.html', title = "The Puppy Manager")
    adopter = session.query(Adopter).filter_by(id = adopter_id).first()
    puppies = session.query(Puppy).filter_by(adopter_id = adopter_id)
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
        output = render_template('page_head.html', title = "Adopt a Puppy!!!")
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

@app.route('/shelters/<int:shelter_id>/new/', methods=['GET', 'POST'])
def new_puppy(shelter_id):
    """page to create a new menu item."""
    form = NewPuppyForm(request.POST)
    if request.method == "POST" and form.validate():
        new_name = request.form['new_name']
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        if (shelter.maximum_capacity - shelter.current_occupancy) <= 0:
            # flash( "'"+shelter.name+"' is full, and puppy '"+new_name+"' can't be added, sorry :(")
            flash( """
                '{shelter_name}' is full, and the puppy
                '{new_name}' couldn't be added, sorry :(
                """.format(shelter_name=shelter.name, new_name=new_name))
            return redirect(url_for("show_puppies", shelter_id=shelter.id))
        else:
            new_puppy = Puppy( name=new_name, shelter_id=shelter.id )
            session.add(new_puppy)
            session.commit()
            flash( "new puppy '" + new_name + "' added!")
            return redirect(url_for("show_puppies", shelter_id=shelter.id))

    else:
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output = render_template('page_head.html', title = "Add a New Puppy! :D")
        output += render_template('new_puppy.html', shelter = shelter)
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
        output = render_template('page_head.html', title = "The Menu Manager")
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
        output = render_template('page_head.html', title = "The Menu Manager")
        puppy = session.query(Puppy).filter_by(id = puppy_id).first()
        if shelter_id == "n":
            shelter = session.query(Shelter).filter_by(id = puppy.shelter_id).first()
        else:
            shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output += render_template( 'delete_puppy.html',
                                   puppy = puppy,
                                   shelter = shelter )
        return output


###############
#adopters CRUD
###############

@app.route('/adopters/')
def show_adopters():
    output = render_template('page_head.html', title = "The State Adopter Manager")
    adopters = session.query(Adopter).all()
    output += render_template('show_adopters.html')
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
        output = render_template('page_head.html', title = "Add a New Adopter! XD")
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
        output = render_template('page_head.html', title = "Edit a Adopter")
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
        output = render_template('page_head.html', title = "Delete an Adopter")
        adopter = session.query(Adopter).filter_by(id = adopter_id).first()
        output += render_template( 'delete_adopter.html', adopter = adopter )
        return output

#Attempt at an API endpoint (GET Req)
@app.route('/shelters/<int:shelter_id>/menu/<int:puppy_id>/JSON/')
def puppyJSON(shelter_id, puppy_id):
    shelter = session.query(Shelter).filter_by(id = shelter_id).one()
    puppy = session.query(Puppy).filter_by(shelter_id = shelter_id).filter_by(id = puppy_id).one()
    return jsonify(Puppy = puppy.serialize)


#Attempt at an API endpoint (GET Req)
@app.route('/shelters/<int:shelter_id>/menu/JSON/')
def show_puppies_JSON(shelter_id):
    shelter = session.query(Shelter).filter_by(id = shelter_id).one()
    puppies = session.query(Puppy).filter_by(shelter_id = shelter_id).all()
    return jsonify(Puppies = [puppy.serialize for puppy in puppies])
