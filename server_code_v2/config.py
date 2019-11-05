import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    PGHOST='127.0.0.1'
    PGDATABASE='display_msg_details'
    PGUSER='admin'
    PGPASSWORD='admin123'