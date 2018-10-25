from flask.cli import FlaskGroup

from project import app, db

cli = FlaskGroup(app)

if __name__ == '_main__':
    cli()
