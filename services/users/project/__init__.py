import os

import click

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

import unittest

app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# instantiate the db
db = SQLAlchemy(app)  # new

# model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'haha': 'hi there'
        })

@click.command('recreate_db')
@with_appcontext
def recreate_db_init():
    db.drop_all()
    db.create_all()
    db.session.commit()

@click.command('test')
@with_appcontext
def test_init():
    """ Runs the tests without code coverage"""
    """ test path should be a directory that contains the tests you want to run, not the path to a single module. """
    """ Try just using . as the directory (assuming you're running it from the top-level project/app directory) and see if that helps. """
    tests = unittest.TestLoader().discover('.', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

def init_app(app):
    app.cli.add_command(recreate_db_init)
    app.cli.add_command(test_init)

init_app(app)
