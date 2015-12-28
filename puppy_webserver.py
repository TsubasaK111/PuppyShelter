from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppy_db_setup import Base, Shelter, Puppy, Puppy_Profile, Adopter

import pdb
import pprint


app = Flask(__name__)


engine = create_engine('sqlite:///puppyShelters.db')
Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()


@app.route('/shelters/')
def index():
    output = render_template('page_head.html', title = "The County Shelter Manager")
    shelters = session.query(Shelter).all()
    for shelter in shelters:
        puppies = session.query(Puppy).filter_by(shelter_id = shelter.id)
        output += render_template( 'puppy_roster.html',
                                   shelter=shelter,
                                   puppies=puppies )
        output += "<br><br>BREAKBREAKBREAK<br><br>"
    return output


@app.route('/shelters/<int:shelter_id>/')
def sheltered_puppies(shelter_id):
    output = render_template('page_head.html', title = "The Shelter Manager")
    shelter = session.query(Shelter).filter_by(id = shelter_id).first()
    puppies = session.query(Puppy).filter_by(shelter_id = shelter_id)
    output += render_template( 'puppy_roster.html',
                               shelter=shelter,
                               puppies=puppies )
    return output


@app.route('/shelters/<int:shelter_id>/new/', methods=['GET', 'POST'])
def new_puppy(shelter_id):
    """page to create a new menu item."""

    if request.method == "POST":
        new_name = request.form['new_name']
        print "\nnew_puppy POST triggered, name is: ", new_name
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        new_puppy = Puppy( name=new_name,
                                shelter_id=shelter.id )
        session.add(new_puppy)
        session.commit()
        flash( "new puppy '" + new_name + "' added!")
        print "POST worked!"
        return redirect(url_for("sheltered_puppies", shelter_id=shelter.id))

    else:
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        output = render_template('page_head.html', title = "Add a New Puppy! :D")
        output += render_template('new_puppy.html', shelter = shelter)
        return output


@app.route('/shelters/<int:shelter_id>/<int:puppy_id>/edit/', methods=['GET', 'POST'])
def edit_puppy(shelter_id, puppy_id):
    """page to edit a puppy's basic information."""
    # return "edit_puppy!"
    if request.method == "POST":
        edited_name = request.form['edited_name']
        print "\nedit_puppy POST triggered, name is: ", edited_name
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
        return redirect(url_for("sheltered_puppies", shelter_id=shelter_id))

    else:
        output = render_template('page_head.html', title = "The Menu Manager")
        print "\nshelters/shelter_id/puppy_id/edit accessed..."
        shelter = session.query(Shelter).filter_by(id = shelter_id).first()
        puppy = session.query(Puppy).filter_by(id = puppy_id).first()
        output += render_template('edit_puppy.html',
                                  shelter = shelter,
                                  puppy = puppy )
        return output


@app.route('/shelters/<int:shelter_id>/<int:puppy_id>/delete/', methods=["GET","POST"])
def delete_puppy(shelter_id, puppy_id):
    """page to delete a puppy."""
    return "delete_puppy!"
#     if request.method == "POST":
#         print "\ndeleteMenuItem POST triggered!, puppy_id is: ", puppy_id
#         deletedMenuItem = session.query(Puppy).filter_by(id = puppy_id).first()
#         session.delete(deletedMenuItem)
#         session.commit()
#         flash( "item '" + deletedMenuItem.name + "' deleted. Auf Wiedersehen!")
#         return redirect(url_for("sheltered_puppies", shelter_id=shelter_id))
#
#     else:
#         print "shelters/delete accessed..."
#         output = render_template('page_head.html', title = "The Menu Manager")
#         shelter = session.query(Shelter).filter_by(id = shelter_id).first()
#         puppy = session.query(Puppy).filter_by(id = puppy_id).first()
#         output += render_template( 'deleteMenuItem.html',
#                                    puppy = puppy,
#                                    shelter = shelter )
#         return output


# #Another attempt at an API endpoint (GET Req)
# @app.route('/shelters/<int:shelter_id>/menu/<int:puppy_id>/JSON/')
# def puppyJSON(shelter_id, puppy_id):
#     shelter = session.query(Shelter).filter_by(id = shelter_id).one()
#     puppy = session.query(Puppy).filter_by(shelter_id = shelter_id).filter_by(id = puppy_id).one()
#     return jsonify(Puppy = puppy.serialize)
#
#
# #A first attempt at an API endpoint (GET Req)
# @app.route('/shelters/<int:shelter_id>/menu/JSON/')
# def sheltered_puppies_JSON(shelter_id):
#     shelter = session.query(Shelter).filter_by(id = shelter_id).one()
#     puppies = session.query(Puppy).filter_by(shelter_id = shelter_id).all()
#     return jsonify(Puppies = [puppy.serialize for puppy in puppies])


if __name__ == "__main__":
    app.secret_key = "ZUPA_SECRET_KEY!!!"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5001)
