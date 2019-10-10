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
import credentials as creds
import psycopg2
import sys, os
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import json
import time
#--------------------------------------REQUIREMENTS--------------------------------------

#--------------------------------------SETTINGS------------------------------------------
NUMBER_OF_RESULTS = 5

#--------------------------------------SETTINGS------------------------------------------

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return('Main Site Goes Here')


#This function creates a table table, if it does not yet exist
def create_table(table_name,table_creation_sql):
    #Check if the database exists. If not, create it
    current_tables = pd.read_sql("SELECT * FROM information_schema.tables",conn)
    exists = False
    for name in current_tables['table_name']:
        if name == table_name:
            exists = True
    if not exists:
        print(table_name,'does not exist, creating',table_name)
        # Sample SQL
        #'CREATE TABLE sessions (id SERIAL, session_id CHARACTER(255), username CHARACTER(255), info JSONB, results JSONB, PRIMARY KEY(id));'
        crsr.execute(table_creation_sql)
        conn.commit()
        print('Done')
    else:
        print(table_name,'already exists, moving on')


#The below function connects to PostgreSQL and also creates the necessary tables, should they be missing
def connect():
    # Set up a connection to the postgres server.
    print("Connecting to the postgres server")
    conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
    +" password="+ creds.PGPASSWORD
    global conn
    global crsr
    conn =psycopg2.connect(conn_string)
    print("Connected!")
    crsr = conn.cursor()
    #Craft the SQL for making the necessary tables
    msg_details_sql = 'CREATE TABLE msg_details (id SERIAL, msg CHARACTER(10485760), msg_start_time timestamp, msg_end_time timestamp, importance smallint, board_id smallint PRIMARY KEY(id));'
    usr_details_sql = 'CREATE TABLE usr_details (id SERIAL, username CHARACTER(255), board_id_permissions json, PRIMARY KEY(id));'
    display_details_sql = 'CREATE TABLE display_details (id SERIAL, ip_address CHARACTER(255), additional_details json, PRIMARY KEY(id));'
    
    #Make the tables
    create_table('msg_details',msg_details_sql)
    create_table('usr_details',usr_details_sql)
    create_table('display_details',display_details_sql)

    #

    


if __name__ == '__main__':
    #Connect to the database
    connect()
    #Run the App
    app.run(host='0.0.0.0', debug=True, use_reloader=False,port = 5000)
    