from flask import Flask
from app.database import init_db


def create_app():

    app = Flask(__name__)

    # database settings
    app.config.from_pyfile('dbconfig.cfg')
    init_db(app)

    return app


app = create_app()
