from flask import render_template, request
from sqlalchemy import and_, or_
from src import app
from src.models import Home

# あいまい検索用のconst
ambiguous_items = ["price", "station_distance", "age"]
price_class = [0, 50000, 60000, 70000, 80000, 90000, 100000, 999999999]
station_distance_class = [0, 5, 10, 15, 20, 25, 999999999]
age_class = [0, 10, 20, 30, 40, 50, 60, 999999999]


@app.route('/', methods=['GET'])
def index():
    homes = Home.query.all()
    result_num = len(homes)
    return render_template("index.html", homes=homes, result_num=result_num, search_flag=False)


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

    if result_num == 0:
        return render_template("index.html", homes=[], result_num=result_num, search_flag=True)

    # あいまい検索
    # hashに変換
    homes = [{"model": home, "point": 0} for (home) in result_homes]

    # 得点の計算
    for ai in ambiguous_items:
        for h in homes:
            h["point"] += calc_weight(h["model"], ai)

    # 点数の高い順に上から表示できるようにする
    homes = sorted(homes, key=lambda x: x["point"], reverse=True)

    return render_template("index.html", homes=homes, result_num=result_num, search_flag=True)


# methodの切り出し
def calc_weight(home, name):
    key = request.form.get(name)
    weight = request.form.get(name + '_weight')

    point = 0

    if not weight == "0":
        # 検索条件との一致度を確認
        if (getattr(home, name) > eval(eval("name + '_class[' + key + ']'"))
            and
                getattr(home, name) <= eval(eval("name + '_class[' + str(int(key)+1) + ']'"))):
            point += 1

        # 重み付け処理
        point = point * int(weight)/100

    return point


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
