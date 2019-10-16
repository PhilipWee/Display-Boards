from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Optional

class newMessageForm(FlaskForm):
    msg = TextAreaField('Insert Message Here', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', validators=[Optional()])
    end_time = DateTimeField('End Time', validators=[Optional()])
    repeat = SelectField('Repeat', choices=[('daily', 'Daily'),
                                            ('never', 'Never'),
                                            ('weekly', 'Weekly'),
                                            ('monthly', 'Monthly'),
                                            ('yearly', 'Yearly')])
    show_time = SelectField('Show Time', choices=[('keep_current_setting', 'Keep Current Setting'),
                                            ('true', 'True'),
                                            ('false', 'False')])
    submit = SubmitField('Create Message')