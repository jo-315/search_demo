from flask import render_template, request
from sqlalchemy import and_, or_
from src import app
from src.models import Home


@app.route('/', methods=['GET'])
def index():
    homes = Home.query.all()
    result_num = len(homes)
    return render_template("index.html", homes=homes, result_num=result_num)


# 検索実行method
# 検索結果はlist型で管理する
@app.route('/search', methods=['POST'])
def post():
    # 確定検索
    name = request.form.get('name')
    address = request.form.get('address')
    layout = request.form.getlist('layout')
    structure = request.form.getlist('structure')
    result_homes = Home.query.filter(
        or_(
            Home.name == name,
            and_(
                Home.address == address if address else True,
                Home.layout.in_(layout) if layout else True,
                Home.structure.in_(structure) if structure else True
            )
        )
    ).all()
    result_num = len(result_homes)

    # あいまい検索
    # hashに変換
    homes = [{"model": home, "point": 0} for (home) in result_homes]

    # 点数の高い順に上から表示できるようにする
    homes = sorted(homes, key=lambda x: x["point"], reverse=True)

    return render_template("index.html", homes=homes, result_num=result_num)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
