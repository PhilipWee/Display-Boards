from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Optional

class newMessageForm(FlaskForm):
    msg = TextAreaField('Insert Message Here', validators=[DataRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    repeat = SelectField('Repeat', choices=[('permanantly', 'Permanantly'),
                                            ('daily', 'Daily'),
                                            ('never', 'Never'),
                                            ('weekly', 'Weekly'),
                                            ('monthly', 'Monthly'),
                                            ('yearly', 'Yearly')])
    
    submit = SubmitField('Create Message')

class newShowTimeForm(FlaskForm):
    show_time = SelectField('Show Time', choices=[('keep_current_setting', 'Keep Current Setting'),
                                            ('true', 'True'),
                                            ('false', 'False')])
    
    submit = SubmitField('Confirm Setting')