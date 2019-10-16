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
from display_msg_funcs import print_msg, time_handler
#--------------------------------------REQUIREMENTS--------------------------------------


app = Flask(__name__)
CORS(app)

#Create a time handle to display the time
time_handle = time_handler()

@app.route('/display_message', methods = ['POST'])
def display_message():
    #Message details are stored under 'msg' key
    content = request.get_json()
    print_msg(content['msg'])

    #If the display time key is true, then run the time display function
    try:
        print('display_time='+content['display_time'])
        if content['display_time'] == 'true':
            time_handle.show_time = True
            time_handle.show_time_start()
        elif content['display_time'] == 'false':
            time_handle.show_time = False
        else:
            #Do not change the current setting
            pass

    return jsonify({'details':'ok'})




if __name__ == '__main__':
    #Run the App
    app.run(host='0.0.0.0', debug=True, use_reloader=False,port = 5001)
    