from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))


username = 'postgres'

password = '114001'

db_name = 'goodbooks'
host = 'localhost'

port = '5432'


# local config database
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite3:////test.db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
engine_container = db.get_engine(app)

def cleanup(session):
    """
    This method cleans up the session object and also closes the connection pool using the dispose method.
    """
    session.close()
    engine_container.dispose()

from app.routes import *
from app.models import *