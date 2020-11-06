from flask import render_template, request
from sqlalchemy import and_
from src import app
from src.models import Home

# あいまい検索用のconst
ambiguous_items = ["price", "station_distance", "age"]
ambiguous_item_dict = {"price": "値段", "station_distance": "駅までの距離", "age": "築年数"}
price_class = [0, 50000, 60000, 70000, 80000, 90000, 100000, 999999999]
price_label = ["0 ~ 5万", "5万 ~ 6万", "6万 ~ 7万", "7万 ~ 8万", "8万 ~ 9万", "9万 ~ 10万", "10万 ~"]
station_distance_class = [0, 5, 10, 15, 20, 25, 999999999]
station_distance_label = ["0 ~ 5分", "6 ~ 10分", "11 ~ 15分", "16 ~ 20分", "21 ~ 25分", "25分 ~"]
age_class = [0, 10, 20, 30, 40, 50, 60, 999999999]
age_label = ["0 ~ 10年", "11 ~ 20年", "21 ~ 30年", "31 ~ 40年", "41 ~ 50年", "51 ~ 60年", "60年 ~"]


@app.route('/', methods=['GET'])
def index():
    homes = Home.query.all()
    result_num = len(homes)
    return render_template("index.html", homes=homes, result_num=result_num, search_flag=False)


# 検索実行method
# 検索結果はlist型で管理する
@app.route('/search', methods=['POST'])
def post():
    # 検索条件をフロントエンドに渡す
    search_conditions = []

    # 確定検索
    name = request.form.get('name')
    search_conditions.append(['名前', name]) if name else True
    address = request.form.get('address')
    search_conditions.append(['住所', address]) if address else True
    layout = request.form.getlist('layout')
    search_conditions.append(['間取り', ' '.join(layout)]) if layout else True
    structure = request.form.getlist('structure')
    search_conditions.append(['構造', ' '.join(structure)]) if structure else True

    result_homes = Home.query.filter(
        and_(
            Home.name == name if name else True,
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
    for ai_name in ambiguous_items:
        key = request.form.get(ai_name)
        weight = request.form.get(ai_name + '_weight')

        # 指定がなかった場合は、ポイントを加算する
        if key == "null":
            for h in homes:
                h["point"] += 1
        # weightが0のときはポイントは加算しない
        elif not weight == "0":
            search_conditions.append([ambiguous_item_dict[ai_name], ' '.join([eval(eval("ai_name + '_label[' + key + ']'")), '重要度', weight, '%'])])
            for h in homes:
                h["point"] += calc_weight(h["model"], ai_name, key, weight)

    # 点数の高い順に上から表示できるようにする
    homes = sorted(homes, key=lambda x: x["point"], reverse=True)

    print(search_conditions)

    # TODO ポイントの規格化（最大は100にする）

    return render_template("index.html", homes=homes, result_num=result_num, search_flag=True, search_conditions=search_conditions)


# 管理者ページ
@app.route('/admin', methods=['GET'])
def admin():
    return render_template("admin.html")


# データセット追加
@app.route('/data_form', methods=['POST'])
def data():
    return


# CSV追加
@app.route('/csv_form', methods=['POST'])
def csv():
    return


# methodの切り出し
def calc_weight(home, name, key, weight):
    point = 0

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
