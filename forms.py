

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length


class AddPetForm(FlaskForm):
    """Pets form """

    name = StringField("Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[("dog", "Dog"),("cat", "Cat"),("snake", "Snake")])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField("Comments", validators=[Optional()])




class EditPetForm(FlaskForm):

    """Form for editing an existing pet."""
    
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])

    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])

    available = BooleanField("Available")