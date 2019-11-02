'''
 Created on Wed Oct 16 2019

 Copyright (c) 2019 Smart Gateway

 Made by Philip Andrew Wee De Wang
'''
#--------------------------------------REQUIREMENTS--------------------------------------
from flask import Flask,jsonify,request,abort, redirect, url_for,render_template
from flask_dance.contrib.github import make_github_blueprint, github
from flask_cors import CORS
from config import Config
import psycopg2
import sys, os
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import json
import time
#--------------------------------------REQUIREMENTS--------------------------------------

#This function creates a table table, if it does not yet exist
def create_table(table_name,table_creation_sql):
    crsr = conn.cursor()
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
    crsr.close()

#The below function connects to PostgreSQL and also creates the necessary tables, should they be missing
def connect():
    # Set up a connection to the postgres server.
    print("Connecting to the postgres server")
    conn_string = "host="+ Config.PGHOST +" port="+ "5432" +" dbname="+ Config.PGDATABASE +" user=" + Config.PGUSER \
    +" password="+ Config.PGPASSWORD
    global conn
    conn =psycopg2.connect(conn_string)
    print("Connected!")
    #Craft the SQL for making the necessary tables
    msg_details_sql = 'CREATE TABLE msg_details (id SERIAL, msg text, msg_start_time text, msg_end_time text, importance smallint, board_id smallint, repeat CHARACTER(255), PRIMARY KEY(id));'
    usr_details_sql = 'CREATE TABLE usr_details (id SERIAL, username CHARACTER(255), board_id_permissions json, PRIMARY KEY(id));'
    display_details_sql = 'CREATE TABLE display_details (id SERIAL, ip_address CHARACTER(255), additional_details text, PRIMARY KEY(id));'
    
    #Make the tables
    create_table('msg_details',msg_details_sql)
    create_table('usr_details',usr_details_sql)
    create_table('display_details',display_details_sql)

#Format strings to sql format
def sql_str(string):
    if string is None:
        return "NULL"
    else:
        result = "'"+str(string)+"'"
        return result

#Add a message to the postgres database
def insert_message(msg, start_time = None, end_time = None, repeat= None, importance = None, board_id = None):
    crsr = conn.cursor()
    sql = "INSERT INTO msg_details(msg, msg_start_time, msg_end_time, importance, board_id, repeat) \
        VALUES \
        ("+sql_str(msg)+", "+sql_str(start_time)+","+sql_str(end_time)+","+sql_str(importance)+","+sql_str(board_id)+","+sql_str(repeat)+");"
    crsr.execute(sql)
    conn.commit()
    crsr.close()

#Add a display board to the postgres database
def add_display_board(ip_address, additional_details = None):
    crsr = conn.cursor()
    sql = "INSERT INTO display_details(ip_address, additional_details) \
        VALUES \
        ("+sql_str(ip_address)+", "+sql_str(additional_details)+");"
    crsr.execute(sql)
    conn.commit()
    crsr.close()

#Remove a message from the postgres database
def rm_message(id):
    crsr = conn.cursor()
    sql = "DELETE FROM msg_details WHERE id = " + str(id)
    crsr.execute(sql)
    conn.commit()
    crsr.close()

#Remove a display board from the postgres database
def rm_display_board(id):
    crsr = conn.cursor()
    sql = "DELETE FROM display_details WHERE id = " + str(id)
    crsr.execute(sql)
    conn.commit()
    crsr.close()

#Get all the calendar data for the messages
def get_calendar_table():
    sql = "SELECT * FROM msg_details"
    result = pd.read_sql(sql,conn)
    return result

#Get all the display board detail
def get_display_table():
    sql = "SELECT * FROM display_details"
    result = pd.read_sql(sql,conn)
    return result

  
