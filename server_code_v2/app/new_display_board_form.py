from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional

class newDisplayBoardForm(FlaskForm):
    target_address = StringField('IP address / Domain of display board')
    details = StringField('Additional Comments')
    submit = SubmitField('Add display board')