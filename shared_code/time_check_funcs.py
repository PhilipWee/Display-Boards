'''
 Created on Fri Nov 01 2019

 Copyright (c) 2019 Smart Gateway

 Made by Philip Andrew Wee De Wang
'''

import datetime
import calendar

#For importing to do test cases
'''
from app.pg_db_funcs import insert_message, get_calendar_table, rm_message

calendar_table = get_calendar_table()
test_cases = [(row['msg_start_time'].strip(),row['msg_end_time'],row['repeat'].strip()) for row_no,row in calendar_table.iterrows()]
'''

#Take note to remember to strip the repeat column when using the function, as there is alot of white space
test_cases = [(None, None, 'permanantly'), ('Whole Day', 'Whole Day', 'daily'), ('14:13', '14:13', 'daily'), ('10/31/2019 12:00 AM', '10/31/2019 12:00 AM', 'never'), ('Whole Day', 'Whole Day', 'weekly Days: Sun Fri'), ('14:15', '14:15', 'weekly Days: Sun Fri'), ('14:15', '14:15', 'monthly Days: 1 3'), ('Whole Day', 'Whole Day', 'monthly Days: 2 4'), ('Whole Day', 'Whole Day', 'yearly Days: 2 Months: Oct'), ('Whole Day', 'Whole Day', 'monthly Days: last')]

def convert_str_to_weekday(string):
    weekdays = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    return weekdays.index(string)

def convert_time_to_dttime(string):
    return datetime.datetime.strptime(string,'%H:%M').time()

def convert_dtstr_to_dttime(string):
    return datetime.datetime.strptime(string,'%m/%d/%Y %H:%M %p')

#Check for whether to display the message for 'permanant'
def check_perma(start,end,repeat,time=datetime.datetime.now()):
    return True

#Check for whether to display the message for 'daily'
def check_daily(start,end,repeat,time=datetime.datetime.now()):
    if start == 'Whole Day':
        return True
    else:
        dt_start = convert_time_to_dttime(start)
        dt_end = convert_time_to_dttime(end)
        if time.time() >= dt_start and time.time() <= dt_end:
            return True
        else:
            return False

#Check for whether to display the message for 'never'
def check_never(start,end,repeat,time=datetime.datetime.now()):
    dt_start = convert_dtstr_to_dttime(start)
    dt_end = convert_dtstr_to_dttime(end)
    if time >= dt_start and time<= dt_end:
        return True
    else:
        return False
    
#Check for whether to display the message for 'weekly'
def check_weekly(start,end,repeat,time=datetime.datetime.now()):
    repeat = repeat.split(' ')[2:]
    repeat = [convert_str_to_weekday(x) for x in repeat]
    if time.weekday() in repeat:
        #It is the correct weekday
        return check_daily(start,end,repeat,time=time)
    else:
        return False

#Check for whether to display the message for 'monthly'
def check_monthly(start,end,repeat,time=datetime.datetime.now()):
    repeat = repeat.split(' ')[2:]
    repeat = [int(x) if x != 'last' else -1 for x in repeat]
    is_last_day = False
    #Check if it is the last day of the month
    last_day = calendar.monthrange(time.year,time.month)[1]
    if time.day == last_day:
        is_last_day = True
    if time.day in repeat or (is_last_day and -1 in repeat):
        #It is the day
        return True
    else:
        return False
    
#Check for whether to display the message for 'yearly'
def check_yearly(start,end,repeat,time=datetime.datetime.now()):
    repeat = [x.strip().split(' ') for x in ' '.join(repeat.split(' ')[2:]).split('Months:')]
    repeat_days = 'monthly Days: ' + ' '.join(repeat[0])
    repeat_months = repeat[1]
    if datetime.datetime.strftime(time,'%b') in repeat_months:
        #Correct month, check correct day
        return check_monthly(start,end,repeat_days,time=time)
    else:
        return False
    
#Final function, combining all the functions and checking what type of repeat it is
def check_is_time(start,end,repeat,time=datetime.datetime.now()):
    #Make the function dictionary
    func_dict = {
                'permanantly':check_perma,
                'daily':check_daily,
                'never':check_never,
                'weekly':check_weekly,
                'monthly':check_monthly,
                'yearly': check_yearly
                }
                
    if start is not None:
        start = start.strip()
    if end is not None:
        end = end.strip()
    if repeat is not None:
        repeat = repeat.stip()

    repeat_type = repeat.split(' ')[0]
    return func_dict[repeat_type](start,end,repeat,time=time)

#Function checks

#Permanant
assert check_is_time(*test_cases[1]) == True
#daily
assert check_is_time(*test_cases[2], time = datetime.datetime(2020, 5, 17, 14, 14)) == False
assert check_is_time(*test_cases[2], time = datetime.datetime(2020, 5, 17, 14, 13)) == True
#never
assert check_is_time(*test_cases[3], time = datetime.datetime(2019, 10, 31, 14, 13)) == False
assert check_is_time(*test_cases[3], time = datetime.datetime(2019, 10, 31, 12, 00)) == True
#weekly
assert check_is_time(*test_cases[4], time = datetime.datetime(2019, 11, 1, 12, 00)) == True
assert check_is_time(*test_cases[4], time = datetime.datetime(2019, 11, 2, 12, 00)) == False
assert check_is_time(*test_cases[5], time = datetime.datetime(2019, 11, 1, 12, 00)) == False
assert check_is_time(*test_cases[5], time = datetime.datetime(2019, 11, 1, 14, 15)) == True
#monthly
assert check_is_time(*test_cases[6], time = datetime.datetime(2019, 11, 1, 14, 15)) == True
assert check_is_time(*test_cases[6], time = datetime.datetime(2019, 11, 3, 14, 15)) == True
assert check_is_time(*test_cases[6], time = datetime.datetime(2019, 11, 2, 14, 15)) == False
assert check_is_time(*test_cases[9], time = datetime.datetime(2019, 12, 31, 14, 15)) == True
assert check_is_time(*test_cases[9], time = datetime.datetime(2019, 12, 30, 14, 15)) == False
assert check_is_time(*test_cases[9], time = datetime.datetime(2019, 11, 30, 14, 15)) == True
#yearly
assert check_is_time(*test_cases[8], time = datetime.datetime(2019, 11, 2, 14, 15)) == False
assert check_is_time(*test_cases[8], time = datetime.datetime(2019, 10, 2, 14, 15)) == True
assert check_is_time(*test_cases[8], time = datetime.datetime(2019, 10, 3, 14, 15)) == False

