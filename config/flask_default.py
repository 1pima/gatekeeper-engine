from os import environ as e

from flask.cli import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI=e['DB_DSN']
SECRET_KEY=e['SECRET_KEY']

SQLALCHEMY_TRACK_MODIFICATIONS=False
