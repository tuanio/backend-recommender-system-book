from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

username = os.environ['PGUSER']
password = os.environ['PGPASSWORD']
db_name = os.environ['PGDATABASE']
host = os.environ['PGHOST']
port = os.environ['PGPORT']
uri = os.environ['DATABASE_URL']

# local config database
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
# app.config['SQLALCHEMY_DATABASE_URI'] = uri

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