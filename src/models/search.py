from src.database import db

# search_type: ラジオボタン→0 プルダウン→1


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    search_type = db.Column(db.Integer, nullable=False)
