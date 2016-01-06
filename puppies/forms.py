from wtforms import Form, BooleanField, StringField, DateField, validators

class NewPuppyForm(Form):
    name = StringField("Name", [validators.InputRequired, validators.length(min=2, max=50)])
    gender = StringField("Gender", [validators.length(min=4, max=7)])
    weight = StringField("Weight")
    dateOfBirth = DateField("Date of Birth", format='%m/%d/%y')
    shelter = StringField("Sheltered in:", [validators.InputRequired])
