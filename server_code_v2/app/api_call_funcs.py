'''
 Created on Wed Oct 16 2019

 Copyright (c) 2019 Smart Gateway

 Made by Philip Andrew Wee De Wang
'''

import requests

def inform_api(msg, destination_ip_and_port, **kwargs):
    dictToSend = {'msg':msg}
    #Add the additional keyword arguments
    for key, value in kwargs.items():
        dictToSend[key] = value
    print('Attempting to send post request to ' + destination_ip_and_port + '/display_message')
    res = requests.post(destination_ip_and_port + '/display_message', json=dictToSend)
    if res.json() == {'details':'ok'}:
        print('sucessfully called API for display')
        return 0
    else:
        print('unsucessful in API call for display')
        return 1
    