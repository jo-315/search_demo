from src.database import db
# from src.models import Search


class Home(db.Model):
    # searchs = Search.query.all()
    # for search in searchs:
    #     ''.format(search.name) = db.Column(db.String(255), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    layout = db.Column(db.String(255), nullable=False)
    station_distance = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    structure = db.Column(db.String(255), nullable=False)
