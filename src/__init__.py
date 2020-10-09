import os
from flask import Flask
from src.database import init_db


def create_app():

    app = Flask(__name__)

    # database settings
    app.config.from_pyfile('dbconfig_%s.py' % os.getenv('FLASK_ENV'))
    init_db(app)

    return app


app = create_app()
