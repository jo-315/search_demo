from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()

        migrate = Migrate(app, db)
        migrate.init_app(app, db)
