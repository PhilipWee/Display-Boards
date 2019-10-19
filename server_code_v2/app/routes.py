from flask import render_template, redirect, request
from app import app
from app.new_message_form import newMessageForm, newShowTimeForm
from app.pg_db_funcs import insert_message, get_calendar_table
from app.api_call_funcs import inform_api

@app.route('/')
@app.route('/index')
def index():
    return redirect('/display-messages', code = 302)


@app.route('/display-messages', methods=["GET","POST"])
def display_messages():
    form = newMessageForm()
    showTimeForm = newShowTimeForm()

    if request.method == "POST" and showTimeForm.validate():
        #Send the message for displaying to the RPI
        try:
            inform_api('', 'http://169.254.186.12:5001', show_time=show_time)
        except:
            print('Warning: Display board uncontactable.')

    if request.method == "POST" and form.validate():
        #Since the form submission is ok, save the message to the database
        msg = form.msg.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        repeat = form.repeat.data
        show_time = form.show_time.data
        #Need to include board id and importance function in future
        importance = None
        board_id = None
        
        #Save the message to postgres
        insert_message(msg,
                        start_time=start_time,
                        end_time=end_time,
                        repeat=repeat,
                        importance=importance,
                        board_id=board_id)
        #Send the message for displaying to the RPI
        try:
            inform_api(msg, 'http://169.254.186.12:5001', show_time=show_time)
        except:
            print('Warning: Display board uncontactable.')

    #Get the calendar table
    data = get_calendar_table()
    tables = [data.to_html(classes='data', header="true")]

    return render_template('display_messages.html',title='Message Configuration Panel', form=form,showTimeForm=showTimeForm tables=tables)

#For API call requesting calendar data
@app.route('/get-calendar-data')
def get_calendar_data():
    #Get the calendar table
    data = get_calendar_table()
    jsonified = data.to_json()
    return jsonified

        