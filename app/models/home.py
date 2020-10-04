from app.models import db


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Intnger(255), nullable=False)
    addres = db.Column(db.String(255), nullable=False)
    layout = db.Column(db.String(255), nullable=False)
