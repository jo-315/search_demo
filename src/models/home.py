from src.database import db


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    addres = db.Column(db.String(255), nullable=False)
    layout = db.Column(db.String(255), nullable=False)
