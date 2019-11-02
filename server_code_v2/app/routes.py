from flask import render_template, redirect, request
from app import app
from app.new_message_form import newMessageForm, newShowTimeForm
from app.pg_db_funcs import insert_message, get_calendar_table, rm_message
from app.api_call_funcs import inform_api


@app.route('/')
@app.route('/index')
def index():
    return redirect('/display-messages', code=302)


@app.route('/display-messages', methods=["GET", "POST"])
def display_messages():
    form = newMessageForm()
    showTimeForm = newShowTimeForm()
    # The warning message gets displayed in case of connection issues, etc
    warning = ""

    if request.method == "POST" and showTimeForm.validate():
        show_time = showTimeForm.show_time.data
        # Send the message for displaying to the RPI
        try:
            inform_api('', 'http://169.254.186.12:5001', show_time=show_time)
        except:
            print('Warning: Display board uncontactable.')

    if request.method == "POST" and form.validate():
        # Since the form submission is ok, save the message to the database
        board_id = form.board_id.data
        importance = form.importance.data
        msg = form.msg.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        once_on_from = form.once_on_from.data
        once_on_to = form.once_on_to.data
        week_days = form.week_days.data
        whole_day = form.whole_day.data
        repeat = form.repeat.data
        day_select = form.day_select.data
        month_select = form.month_select.data

        # Handle each of the different repeat cases
        if repeat == 'permanantly':
            insert_message(msg,
                        repeat=repeat,
                        importance=importance,
                        board_id=board_id)
        
        elif repeat == 'daily':
            if whole_day == 'Y':
                insert_message(msg,
                            start_time='Whole Day',
                            end_time = 'Whole Day',
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
            else:
                insert_message(msg,
                            start_time = start_time,
                            end_time = end_time,
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
        elif repeat == 'never':
            insert_message(msg,
                            start_time = once_on_from,
                            end_time = once_on_to,
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
        elif repeat == 'weekly':
            repeat = repeat + ' Days: ' + ' '.join(week_days)
            if whole_day == 'Y':
                insert_message(msg,
                            start_time='Whole Day',
                            end_time = 'Whole Day',
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
            else:
                insert_message(msg,
                            start_time = start_time,
                            end_time = end_time,
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
        elif repeat == 'monthly':
            repeat = repeat + ' Days: ' + ' '.join(day_select)
            if whole_day == 'Y':
                insert_message(msg,
                            start_time='Whole Day',
                            end_time = 'Whole Day',
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
            else:
                insert_message(msg,
                            start_time = start_time,
                            end_time = end_time,
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
        elif repeat == 'yearly':
            repeat = repeat + ' Days: ' + ' '.join(day_select) + ' Months: ' + str(month_select)
            if whole_day == 'Y':
                insert_message(msg,
                            start_time='Whole Day',
                            end_time = 'Whole Day',
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)
            else:
                insert_message(msg,
                            start_time = start_time,
                            end_time = end_time,
                            repeat=repeat,
                            importance=importance,
                            board_id=board_id)

        
        # Send the message for displaying to the RPI
        try:
            inform_api(msg, 'http://169.254.186.12:5001')

        except:
            print('Warning: Display board uncontactable.')
            warning="Warning: Display board uncontactable. \
                 Please check the internet connection of the display board. \
                 The display board will be updated once it regains connection."

    # Get the calendar table
    data=get_calendar_table()

    return render_template('display_messages.html',
                           title = 'Message Configuration Panel',
                           form = form,
                           showTimeForm = showTimeForm,
                           column_names = data.columns.values,
                           row_data = list(data.values.tolist()),
                           link_column = "id",
                           zip = zip,
                           warning = warning)

# For API call requesting calendar data
@app.route('/get-calendar-data')
def get_calendar_data():
    # Get the calendar table
    data=get_calendar_table()
    jsonified=data.to_json()
    return jsonified

# For handling the removal of messages
@app.route('/delete-msg', methods = ["POST"])
def delete_msg():
    # Remove the appropriate message from the table
    try:
        rm_message(request.form['id'])
        print("Successfully removed message")
        return '0'
    except:
        print("Error: Unable to remove message from postgres database")
        return '1'
