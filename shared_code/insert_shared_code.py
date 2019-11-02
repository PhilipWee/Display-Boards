'''
 Created on Sat Nov 02 2019

 Copyright (c) 2019 Smart Gateway

 Made by Philip Andrew Wee De Wang

Use this module when editing the shared code functions.
This will ensure that the other files within this directory are 
pasted into the rpi_api_code and server_code_v2 folders and ensures 
consistency throughout
'''

from shutil import copy
import os
import pathlib

dir_path = os.path.dirname(os.path.realpath(__file__))

print(os.listdir(dir_path))

def dest_path_creator(relative_path_from_parent):
    return os.path.join(pathlib.Path(dir_path).parent,relative_path_from_parent)

for file_name in os.listdir(dir_path):
    if file_name != 'insert_shared_code.py':
        #Copy and paste the code as necessary
        file_path = os.path.join(dir_path,file_name)
        destination_path = dest_path_creator(os.path.join('rpi_api_code','shared'))
        destination_path2 = dest_path_creator(os.path.join('server_code_v2','app','shared'))
        copy(file_path,destination_path)
        copy(file_path,destination_path2)

