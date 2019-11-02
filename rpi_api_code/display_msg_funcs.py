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

#------------------------SETTINGS----------------------------------
CHARACTERLIMIT = 16
HOSTURL = 'http://169.254.228.228:5000/'
#------------------------SETTINGS----------------------------------

is_rpi = True
#Check if it is an rpi and set up the environment if so
try:
    if os.uname().nodename == 'raspberrypi':    
            
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

except:
    is_rpi = False

#This function is for printing a message for a 16x2 LCD
#Add to this function to handle different display board types
def print_msg(msg):
    if is_rpi:
        client.set('msg',msg)
    else:
        print(msg)
        
#This function is for clearing the 16x2 LCD
#Add to this function to handle different display board types
def clear_lcd():
    lcd.clear()


#The time handler continuously updates the time or scrolls the message if necessary
class time_handler():

    #This function continuously displays the time
    def show_time_instance(self):
        msg = ''
        i = 0
        scrolling = False
        while True:
            to_print = ''
            
            #Handle the message
            try:
                new_msg = client.get('msg').decode("utf-8").replace('\n','').replace('\r','').strip()
            except:
                new_msg = ''
                
            if msg != new_msg:
                msg = new_msg
                if msg == '':
                    clear_lcd()
                if len(msg) > CHARACTERLIMIT:
                    scrolling = True
                else:
                    scrolling = False
                    
            if scrolling == True:
                to_print += (msg+' '+msg)[i:CHARACTERLIMIT+i]
                i += 1
                if i>CHARACTERLIMIT+1:
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
            lcd.message = to_print
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
        print('Attempting to retrieve data from', HOSTURL)
        data = pd.read_json(url)
        #Save the data to csv in case the server goes down
        data.to_csv(os.path.dirname(os.path.abspath(__file__)) + '/msg_data.csv')
    except:
        print('Failed, attempting to read from csv')
        data = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/msg_data.csv')
        data['msg_start_time'] = pd.to_datetime(data['msg_start_time'])
        data['msg_end_time'] = pd.to_datetime(data['msg_end_time'])
    
    return data

#Create a function that determines the message to be displayed
def get_msg(url = HOSTURL):
    data = get_message_df(url)
    print(data.head())
    msg_array = []
    #Remove the irrelevant rows
    for row_no,row in data.iterrows():
        start = row['msg_start_time']
        end = row['msg_end_time']
        repeat = row['repeat']
        if check_is_time(start,end,repeat):
            msg_array.append((row['msg'],row['importance']))
    #Sort the messages by importance
    msg_array = sorted(msg_array, key=lambda result:result[1])
    msg = ' '.join([x[0] for x in msg_array])
    client.set('msg',msg)
    print(msg)
    return msg

#Start memcache to store info like whether to display the time, etc
client = base.Client(('localhost',11211))
#Intialise by connecting to the host
print(get_msg())

    
