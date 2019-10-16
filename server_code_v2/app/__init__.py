from flask import Flask
from config import Config
import app.pg_db_funcs

app.pg_db_funcs.connect()
app = Flask(__name__)
app.config.from_object(Config)

from app import routes