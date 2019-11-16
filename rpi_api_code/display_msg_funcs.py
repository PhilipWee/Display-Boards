'''
 Created on Wed Oct 16 2019

 Copyright (c) 2019 Smart Gateway

 Made by Philip Andrew Wee De Wang
'''


import os
import multiprocessing
import time
from datetime import datetime
import sys
from pymemcache.client import base
import requests
import pandas as pd
from math import ceil
from shared.time_check_funcs import check_is_time
import json

#------------------------SETTINGS----------------------------------
CHARACTERLIMIT = 16
HOSTURL = 'http://127.0.0.1:5000'
DISPLAY_TYPE = 'test' #Types: test (testing) small (Philip's board) big (on site)
#------------------------SETTINGS----------------------------------

is_rpi = True
#Check if it is an rpi and set up the environment if so
if DISPLAY_TYPE == 'small':    
        
    #!/usr/bin/python
    # Example using a character LCD connected to a Raspberry Pi
    import time
    import board
    import digitalio
    import adafruit_character_lcd.character_lcd as character_lcd

    # Raspberry Pi pin setup
    lcd_rs = digitalio.DigitalInOut(board.D26)
    lcd_en = digitalio.DigitalInOut(board.D19)
    lcd_d7 = digitalio.DigitalInOut(board.D11)
    lcd_d6 = digitalio.DigitalInOut(board.D5)
    lcd_d5 = digitalio.DigitalInOut(board.D6)
    lcd_d4 = digitalio.DigitalInOut(board.D13)
    lcd_backlight = digitalio.DigitalInOut(board.D2)

    LCD_RS = 26
    LCD_E  = 19
    LCD_D4 = 13 
    LCD_D5 = 6
    LCD_D6 = 5
    LCD_D7 = 11


    # Define LCD column and row size for 16x2 LCD.
    lcd_columns = 16
    lcd_rows = 2

    lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

elif DISPLAY_TYPE == 'test':
    is_rpi = False

#This function is for printing a message for a 16x2 LCD
#Add to this function to handle different display board types
def print_msg(msg):
    if is_rpi:
        lcd.message = msg
    else:
        print(msg)
        
#This function is for clearing the 16x2 LCD
#Add to this function to handle different display board types
def clear_lcd():
    if is_rpi:
        lcd.clear()


#The time handler continuously updates the time or scrolls the message if necessary
class time_handler():

    #This function continuously displays the time
    def show_time_instance(self):
        msg = ''
        i = 0
        scrolling = False
        current_min = datetime.now().minute
        while True:
            to_print = ''
            #If it is a new minute, run get msg
            if current_min != datetime.now().minute:
                current_min = datetime.now().minute
                #Sometimes does not work due to threading. Hence try except block
                get_msg()


            #Handle the message
            try:
                new_msg = client.get('msg').decode("utf-8").replace('\n','').replace('\r','').strip()
            except:
                new_msg = ''
                
            if msg != new_msg:
                msg = new_msg
                clear_lcd()
                if len(msg) > CHARACTERLIMIT:
                    scrolling = True
                else:
                    scrolling = False
                    
            if scrolling == True:
                to_print += (msg+' '+msg)[i:CHARACTERLIMIT+i]
                i += 1
                if i>len(msg)+CHARACTERLIMIT+1:
                    i = 0
            elif scrolling == False:
                to_print += msg
            
            #Handle showing the time
            if client.get('show_time_bool') == b'True':
                to_print += "\n Time: %s" %time.strftime("%H:%M:%S")
            elif client.get('show_time_bool') == b'False':
                pass
            
            print('Full Message: ', msg.encode())
            print('Printed Message: ',to_print)
            #Set the lcd display
            print_msg(to_print)
            sys.stdout.flush()
            time.sleep(0.5)
            

    #Create the thread that constant prints the time
    def __init__(self):
        client.set('show_time_bool',True)
        client.set('msg','')
        self.time_process = multiprocessing.Process(target=self.show_time_instance)


    #This function handles the time thread
    def show_time(self, show):
        if show == True:  
            client.set('show_time_bool',True)
        elif show == False:
            client.set('show_time_bool',False)
        print(client.get('show_time_bool'))


#Create a new function to get the message data table
def get_message_df(url = HOSTURL):
    url = url + '/get-calendar-data'
    try:
        print('Attempting to retrieve calendar data from', url)
        data = pd.read_json(url, convert_dates = False)
        print(data['msg_start_time'])
        #Save the data to csv in case the server goes down
        data.to_csv(os.path.dirname(os.path.abspath(__file__)) + '/msg_data.csv')
    except:
        print('Failed, attempting to read from csv')
        data = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/msg_data.csv')
    
    return data

def get_display_df(url = HOSTURL):
    url = url + '/get-display-data'
    try:
        print('Attempting to retrieve display data from', url)
        data = pd.read_json(url, convert_dates = False)
        #Save the data to csv in case the server goes down
        data.to_csv(os.path.dirname(os.path.abspath(__file__)) + '/display_data.csv')
    except:
        print('Failed, attempting to read from csv')
        data = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/display_data.csv')
    
    return data

def register_board(url = HOSTURL):
    with open(os.path.dirname(__file__)+"/board_id.txt","a+") as f:
        f.seek(0,0)
        details = f.readlines()
        if details != []:
            (board_id,description) = (detail.strip() for detail in details)
        else:
            board_id = input('Please enter an ID for the board: ')
            description = input('Please enter a description for the board: ')
            f.write(board_id +'\n' + description)
        print('board_id:',board_id)
        print('description:',description)
    client.set('board_id',board_id)
    client.set('description',description)
    #Inform the server of the new board that has been set up
    headers = {'content-type': 'application/json'}
    result = requests.post(url+'/manage-display-boards', json.dumps({'board_id':board_id,'description':description}), headers=headers)
    print(result.json())

#Create a function that determines the message to be displayed
def get_msg(url = HOSTURL):
    data = get_message_df(url)
    display_data = get_display_df(url)
    display_data = display_data[display_data['id'].apply(lambda x:x.strip()) == client.get('board_id').decode('utf-8')]
    print(display_data)
    if display_data['display_time'].values[0] == False:
        client.set('show_time_bool',False)
    elif display_data['display_time'].values[0] == True:
        client.set('show_time_bool',True)
    print(data.head())
    
    msg_array = []
    #Slice the dataframe so only those with the current board's ID are accepted
    data = data[data['board_id'].apply(lambda x:x.strip()) == client.get('board_id').decode('utf-8')]
    print(data.head())
    #Remove the irrelevant rows
    for _,row in data.iterrows():
        start = row['msg_start_time']
        end = row['msg_end_time']
        repeat = row['repeat']
        #Make sure the time of the function is updated as of the time of running the function
        if check_is_time(start,end,repeat,time = datetime.now()):
            msg_array.append((row['msg'],row['importance']))
    #Sort the messages by importance
    msg_array = sorted(msg_array, key=lambda result:result[1])
    msg = ' '.join([str(x[0]) for x in msg_array])
    client.set('msg',msg.encode('ascii',errors='ignore'))
    #print(msg)
    return msg

#Start memcache to store info like whether to display the time, etc
client = base.Client(('localhost',11211))
#Intialise by connecting to the host
print(get_msg())
register_board()
    
