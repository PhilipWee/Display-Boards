'''
 Created on Wed Oct 09 2019

 Copyright (c) 2019 Smart Gateway

 Made by Philip Andrew Wee De Wang
'''

#--------------------------------------REQUIREMENTS--------------------------------------
from flask import Flask,jsonify,request,abort, redirect, url_for,render_template
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
import sys, os
import numpy as np
from display_msg_funcs import get_msg, time_handler, clear_lcd
from pymemcache.client import base
#--------------------------------------REQUIREMENTS--------------------------------------


app = Flask(__name__)
CORS(app)



@app.route('/display_message', methods = ['POST'])
def display_message():
    if request.is_json:
        print(request.get_json())

    #Clear the lcd
    clear_lcd()
    #Get the latest data from the server
    get_msg()
    return jsonify({'details':'ok'})

@app.route('/update_board', methods = ['POST'])
def update_board():
    if request.is_json:
        print(request.get_json())
        try:
            json_data = request.get_json()
            client.set('board_id',str(json_data['board_id']))
        except:
            print('Error in parsing json board_id data')

    #Clear the lcd
    clear_lcd()
    #Get the latest data from the server
    get_msg()
    return jsonify({'details':'ok'})




if __name__ == '__main__':
    #Create a time handle to display the time
    time_handle = time_handler()
    #Manually start the time process
    time_handle.time_process.start()
    #Update self with the latest message.
    #Must be done after initialising time handle because time handle resets the message
    #On initialisation
    get_msg()
    #Run the App
    app.run(host='0.0.0.0', debug=True, use_reloader=False,port = 5001)
    