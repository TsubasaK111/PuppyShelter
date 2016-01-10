from wtforms import Form, BooleanField, StringField, DateField, IntegerField, DecimalField, validators

class NewPuppyForm(Form):
    name = StringField( "Name",
                        [ validators.InputRequired(),
                          validators.Length(min=2, max=50) ])
    gender = StringField("Gender", [validators.Length(min=4, max=7)])
    weight = DecimalField("Weight")
    dateOfBirth = DateField("Date of Birth", format='%m/%d/%y')
    # shelter = StringField( "Sheltered in:",
    #                        [validators.InputRequired()] )
    shelter_id = IntegerField( "Sheltered in:",
                               [validators.InputRequired()])


class NewShelterForm(Form):
    name = StringField( "Shelter Name", [ validators.InputRequired(),
                                          validators.Length(min=10, max=50) ])
    id = IntegerField( "Shelter ID" )
