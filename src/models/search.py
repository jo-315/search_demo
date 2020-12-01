from src.database import db

# search_type: テキスト→0 ラジオボタン→1 プルダウン→2


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255), nullable=False)
    search_order = db.Column(db.Integer, nullable=False)
    search_type = db.Column(db.Integer, nullable=False)
    step = db.Column(db.Integer, nullable=True)
    digit = db.Column(db.Integer, nullable=True)
    unit = db.Column(db.String(255), nullable=True)
    search_min = db.Column(db.Integer, nullable=True)
    search_max = db.Column(db.Integer, nullable=True)
    pull_menu_num = db.Column(db.Integer, nullable=True)
    items = db.Column(db.String(255), nullable=True)
    ambiguous = db.Column(db.Boolean, nullable=False)
