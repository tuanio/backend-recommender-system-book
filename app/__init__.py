from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir  = os.path.abspath(os.path.dirname(__file__))


username = 'postgres'

password = 'hmtoan30'

db_name = 'goodbooks'
host = 'localhost'

port = '5432'


# local config database 
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite3:////test.db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from app.models import * # import all schema table = jls_extract_def()
from app.routes import *