from flask import render_template
from app import app
from app.new_message_form import newMessageForm

@app.route('/')
@app.route('/index')
def index():
    form = newMessageForm()
    return render_template('display_messages.html',title='Message Configuration Panel', form=form)