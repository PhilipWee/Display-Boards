from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired

class newMessageForm(FlaskForm):
    message = TextAreaField('Insert Message Here', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', validators=[DataRequired()])
    end_time = DateTimeField('End Time', validators=[DataRequired()])
    repeat = SelectField('Repeat', choices=[('never', 'Never'),
                                            ('daily', 'Daily'),
                                            ('weekly', 'Weekly'),
                                            ('monthly', 'Monthly'),
                                            ('yearly', 'Yearly')])
    submit = SubmitField('Create Message')