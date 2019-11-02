from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional

class newMessageForm(FlaskForm):
    board_id = SelectField('Board ID', choices=[('1','1')])
    importance = SelectField('Importance', choices = [(str(i),str(i)) for i in range(0,10)])
    msg = TextAreaField('Insert Message Here')
    start_time = StringField('Start Time')
    end_time = StringField('End Time')
    once_on_from = StringField('Display Message from')
    once_on_to = StringField('Display Message to')
    week_days = SelectMultipleField('Week Days to display on (Hold Ctrl to select Multiple)',choices=[(x,x) for x in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']])
    whole_day = SelectField('Whole Day?', choices=[(x,x) for x in ['Y','N']])
    repeat = SelectField('Repeat', choices=[('permanantly', 'Permanantly'),
                                            ('daily', 'Daily'),
                                            ('never', 'Never'),
                                            ('weekly', 'Weekly'),
                                            ('monthly', 'Monthly'),
                                            ('yearly', 'Yearly')])
    day_select = SelectMultipleField('Day(s) to display on (Hold Ctrl to select Multiple)',choices=[(str(x),str(x)) for x in range(1,32)]+[('last','Last Day of Every Month')])
    month_select = SelectField('Month to display on', choices = [(x,x) for x in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']])
    submit = SubmitField('Create Message')

class newShowTimeForm(FlaskForm):
    show_time = SelectField('Show Time', choices=[('keep_current_setting', 'Keep Current Setting'),
                                            ('true', 'True'),
                                            ('false', 'False')])
    
    submit = SubmitField('Confirm Setting')