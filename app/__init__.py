from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():

    app = Flask(__name__)

    # database settings
    app.config.from_pyfile('dbconfig.cfg')
    db = SQLAlchemy(app)
    db.init_app(app)

    return app, db


app, db = create_app()
