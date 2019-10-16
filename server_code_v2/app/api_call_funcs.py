'''
 Created on Wed Oct 16 2019

 Copyright (c) 2019 Smart Gateway

 Made by Philip Andrew Wee De Wang
'''

import requests

def inform_api(msg, destination_ip):
    dictToSend = {'msg':msg}
    res = requests.post(destination_ip + '/endpoint', json=dictToSend)
    if res.json() == {'details':'ok'}:
        print('sucessfully called API for display')
        return 0
    else:
        print('unsucessful in API call for display')
        return 1
    