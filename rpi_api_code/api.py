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
    #Clear the lcd
    clear_lcd()
    #Message details are stored under 'msg' key
    content = request.get_json()
    get_msg()
    #If the display time key is true, then run the time display function
    try:
        print('show_time='+content['show_time'])
        if content['show_time'] == 'true':
            time_handle.show_time(True)
        elif content['show_time'] == 'false':
            time_handle.show_time(False)
        else:
            #Do not change the current setting
            pass
    except:
        pass

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
    