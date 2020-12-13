from src.database import db


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    layout = db.Column(db.String(255), nullable=False)
    station_distance = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    structure = db.Column(db.String(255), nullable=False)
