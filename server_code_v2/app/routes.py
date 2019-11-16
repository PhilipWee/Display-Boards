from flask import render_template, redirect, request
from app import app
from app.new_message_form import newMessageForm, newShowTimeForm
from app.new_display_board_form import newDisplayBoardForm
from app.pg_db_funcs import *
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

    #Get the display boards table to populate the board id
    display_table = get_display_table()
    form.board_id.choices = [(row['id'],row['id']) for row_no,row in display_table.iterrows()]
    showTimeForm.board_id.choices = [(row['id'],row['id']) for row_no,row in display_table.iterrows()]

    if request.method == "POST" and showTimeForm.validate():
        show_time = showTimeForm.show_time.data
        board_id = showTimeForm.board_id.data
        if show_time == 'false':
            show_time = False
        if show_time == 'true':
            show_time = True
        print(show_time)
        # # Send the message for displaying to the RPI
        # try:
        #     inform_api('', 'http://' + display_dict[board_id] + ':5001', show_time=show_time)
        # except:
        #     print('Warning: Display board uncontactable.')
        #Update the board id table
        warning = "Board '" + str(board_id) + "' shows time: " + str(show_time)
        change_display_time(board_id,show_time)

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
        # try:
        #     inform_api(msg, 'http://' + display_dict[board_id] + ':5001')

        # except:
        #     print('Warning: Display board uncontactable.')
        #     warning="Warning: Display board uncontactable. \
        #          Please check the internet connection of the display board. \
        #          The display board will be updated once it regains connection."

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

@app.route('/manage-display-boards', methods=["GET", "POST"])

def manage_display_boards():
    form = newDisplayBoardForm()
    # The warning message gets displayed in case of connection issues, etc
    warning = ""

    if request.method == "POST":
        data = request.get_json()
        print(data)
        # # Since the form submission is ok, save the display board details to the database
        # target_address = form.target_address.data
        # additional_details = form.details.data

        # # Insert the data into the database
        # try:
        return add_display_board(board_id=data['board_id'],additional_details=data['description'])
        # except:
        #     return jsonify({'Error':'Invalid input'})

        #Get the display boards table to populate the board id
        display_table = get_display_table()
        display_dict = {row['ip_address']:row['id'].strip() for row_no,row in display_table.iterrows()}

        inform_api('http://' + target_address + ':5001',extension = '/update_board', board_id = display_dict[target_address])

    # Get the calendar table
    data=get_display_table()

    return render_template('manage_display_boards.html',
                           title = 'Message Configuration Panel',
                           form = form,
                           column_names = data.columns.values,
                           row_data = list(data.values.tolist()),
                           link_column = "id",
                           zip = zip,
                           warning = warning)

# For API call requesting calendar data
@app.route('/get-calendar-data')
def get_calendar_data():
    # # Get the calendar table
    data=get_calendar_table()

    jsonified=data.to_json()
    return jsonified

#For letting the rpi access the display table
@app.route('/get-display-data')
def get_display_table_api():
    data = get_display_table()
    jsonified = data.to_json()
    return jsonified

# For handling the removal of messages
@app.route('/delete-msg', methods = ["POST"])
def delete_msg():
    #Get the display boards table
    display_table = get_display_table()
    display_dict = {row['id']:row['id'].strip() for row_no,row in display_table.iterrows()}

    # Get the calendar table
    data=get_calendar_table()
    print(request.form['id'])
    print(data)
    #Get the board id from the message id
    board_id = data[data['id'] == int(request.form['id'])]['board_id'].values[0]
    print(board_id)
    
    
    # Remove the appropriate message from the table
    try:
        rm_message(request.form['id'])
        
    except:
        print("Error: Unable to remove message from postgres database")
        return '1'
    # Tell the rpi that there is an update
    try:
        # inform_api('message deleted', 'http://' + display_dict[board_id] + ':5001')
        return '0'

    except:
        print('Warning: Display board uncontactable.')
        return '1'

# For handling the removal of display boards
@app.route('/delete-display-board', methods = ["POST"])
def delete_display_board():
    print(request.form['id'])
    # Remove the appropriate message from the table
    try:
        rm_display_board(request.form['id'])
        print("Successfully removed display board")
        return '0'
        
    except:
        print("Error: Unable to remove display board from postgres database")
        return '1'

        
    