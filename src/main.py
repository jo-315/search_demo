import math
import re
from flask import render_template, request
from sqlalchemy import and_
from src import app
from src.models import Home, Search

# あいまい検索用のconst
ambiguous_items = ["price", "station_distance", "age"]
ambiguous_item_dict = {"price": "値段", "station_distance": "駅までの距離", "age": "築年数"}

# 最初の検索画面
@app.route('/', methods=['GET'])
def index():
    # Homeモデルの総数
    homes = Home.query.all()
    result_num = len(homes)

    # 検索項目の準備
    searchs = get_searchs()

    return render_template(
        "search/index.html",
        homes=homes,
        result_num=result_num,
        search_flag=False,
        searchs=searchs
    )


# 検索実行method
# 検索結果はlist型で管理する
@app.route('/search', methods=['POST'])
def post():
    # 検索項目の準備
    searchs = get_searchs()

    # 検索条件をフロントエンドに渡す
    search_conditions = []

    # 検索条件をparamsに格納
    params = []

    # 重要度を格納
    weights = []

    # もし名前で検索されていたらここに名前を入れる
    name = None

    request_items = request.form.to_dict(flat=False)
    for key in request_items.keys():
        if(re.search('.*_weight', key)):  # 重要度の場合
            # TODO 重要度の格納
            weights.append(request_items[key])

        else:  # 検索条件の場合
            if (len(request_items[key]) <= 1):

                value = request_items[key][0]

                if (value == 'null' or len(value) == 0):
                    continue

                # 名前で検索が行われている場合
                if (key == 'name'):
                    name = value

                search_type = Search.query.filter(Search.name_en == key).all()[0].search_type
                if (search_type == 0):  # テキスト
                    params.append(eval('Home.' + key + '==' + value + ')'))

                elif (search_type == 1):  # チェックボックス
                    params.append(eval('Home.' + key + '.in_(["' + value + '"])'))

                elif (search_type == 2):  # プルダウン
                    continue

            else:  # チェックボックスで複数の条件を指定した場合
                values = request_items[key]
                params.append(eval('Home.' + key + '.in_(' + str(values) + ')'))

    results = Home.query.filter(
        and_(
            Home.name == name if name else True,
            and_(*params)
        )
    ).all()
    result_num = len(results)

    if result_num == 0:
        return render_template(
            "search/index.html",
            homes=[],
            result_num=result_num,
            search_flag=True,
            searchs=searchs
        )

    # # あいまい検索
    # # hashに変換
    results = [{"model": result, "point": 0} for (result) in results]

    # # 得点の計算 TODO: あいまい検索についてSearchモデルにデータを入れておく
    # for ai_name in ambiguous_items:
    #     key = request.form.get(ai_name)
    #     weight = request.form.get(ai_name + '_weight')

    #     # 指定がなかった場合は、ポイントを加算する
    #     if key == "null":
    #         for h in homes:
    #             h["point"] += 1
    #     # weightが0のときはポイントは加算しない
    #     elif not weight == "0":
    #         search_conditions.append([
    #             ambiguous_item_dict[ai_name],
    #             ' '.join([eval(eval("ai_name + '_label[' + key + ']'")), '重要度', weight, '%'])
    #         ])
    #         for h in homes:
    #             h["point"] += calc_weight(h["model"], ai_name, key, weight)

    # 点数の高い順に上から表示できるようにする
    # homes = sorted(homes, key=lambda x: x["point"], reverse=True)

    # TODO ポイントの規格化（最大は100にする）

    return render_template(
        "search/index.html",
        homes=results,
        result_num=result_num,
        search_flag=True,
        search_conditions=search_conditions,
        searchs=searchs
    )


# 管理者ページ
@app.route('/admin', methods=['GET'])
def admin():
    searchs = Search.query.all()
    return render_template("admin/admin.html", searchs=searchs)


# データセット追加
@app.route('/data_form', methods=['POST'])
def data():
    return


# CSV追加
@app.route('/csv_form', methods=['POST'])
def csv():
    return


# --- methodの切り出し --- #

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


def get_searchs():
    searchs = Search.query.all()

    for search in searchs:
        if search.search_type == 1:  # チェックボックス
            # 検索項目に該当するデータを全て取得→チェックボックスで全て表示できるように
            items = []
            results = Home.query.distinct(eval('Home.' + search.name_en)).all()

            for result in results:
                items.append(eval('result.' + search.name_en))

            search.items = ",".join(items)

        elif search.search_type == 2:  # プルダウン
            # 該当プロパティのmax・minを取得
            results = Home.query.order_by(eval('Home.' + search.name_en)).distinct(eval('Home.' + search.name_en)).all()

            min = eval('results[0].' + search.name_en)
            max = eval('results[-1].' + search.name_en)

            step = search.step

            # プルダウンのアイテム数を計算 TODO 計算あってるか確認
            pull_menu_num = math.ceil((max - min)/step + 1)

            search.pull_menu_num = pull_menu_num

            # 表示させるのに最適な値に丸める
            search.search_min = math.ceil(min/step - 1) * step
            search.search_max = math.ceil(max/step) * step

            # TODO: 万、億などの桁を丸める

    searchs = sorted(searchs, key=lambda x: x.search_order)

    return searchs


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
