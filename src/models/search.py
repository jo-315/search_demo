from src.database import db

# search_type: 確定検索→0 あいまい検索→1


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    search_type = db.Column(db.Integer, nullable=False)
