import math
import re
from flask import render_template, request
from sqlalchemy import and_
from src import app
from src.models import Home, Search

# 最初の検索画面
@app.route('/', methods=['GET'])
def index():
    # モデルの総数
    results = Home.query.all()
    result_num = len(results)

    # 検索項目の準備
    searchs = get_searchs()

    return render_template(
        "search/index.html",
        results=results,
        result_num=result_num,
        search_flag=False,
        searchs=searchs
    )


# 検索実行method
@app.route('/search', methods=['POST'])
def post():
    # 検索項目の準備
    searchs = get_searchs()

    # 検索された項目をフロントエンドに渡す
    search_conditions = []

    # 検索条件をparamsに格納
    params = []

    # 重要度を格納
    weights = []

    # もし名前で検索されていたらここに名前を入れる
    name = None

    # 検索された項目をフロントエンドから取得
    request_items = request.form.to_dict(flat=False)

    for key in request_items.keys():
        # 重要度の場合
        if(re.search('.*_weight', key)):
            weights.append([key, request_items[key]])

        # 検索条件の場合
        else:
            # チェックボックスで複数の条件を指定した場合
            if (len(request_items[key]) > 1):

                values = request_items[key]

                search_conditions_key = list(filter(lambda x: x.name_en == key, searchs))[0].name
                search_conditions.append([search_conditions_key, ' '.join(values)])

                params.append(eval('Home.' + key + '.in_(' + str(values) + ')'))

            # 指定した条件が一つ
            else:

                value = request_items[key][0]

                if (value == 'null' or len(value) == 0):
                    continue

                search_conditions_key = list(filter(lambda x: x.name_en == key, searchs))[0].name
                search_conditions.append([search_conditions_key, value])

                # 名前で検索が行われている場合
                if (key == 'name'):
                    name = value

                search_type = get_search_type(key)
                if (search_type == 0):  # テキスト
                    params.append(eval('Home.' + key + '==' + value + ')'))

                elif (search_type == 1):  # チェックボックス
                    params.append(eval('Home.' + key + '.in_(["' + value + '"])'))

                elif (search_type == 2):  # プルダウン
                    continue

    # 実際に検索を行う
    results = Home.query.filter(
        and_(
            Home.name == name if name else True,
            and_(*params)
        )
    ).all()

    # ヒット数
    result_num = len(results)

    if result_num == 0:
        return render_template(
            "search/index.html",
            results=[],
            result_num=result_num,
            search_flag=True,
            searchs=searchs
        )

    # 重要度の計算 & あいまい検索 を下で行う

    # hashに変換（ポイントが高いデータが検索によく該当している）
    results = [{"model": result, "point": 0} for (result) in results]

    # 重要度の計算
    for weight_item in list(filter(lambda x: x.weight, searchs)):
        weight_item_name = weight_item.name

        # search_consitions の中から対象とする重要度検索の項目を取り出す
        key = find_in_double_list(weight_item_name, search_conditions)

        # 検索項目に含まれない場合はスキップ
        if not key:
            continue

        weight_item = find_in_double_list(key + '_weight', weights)
        weight = weight_item[1]

        search_conditions.append([
            weight_item_name,
            ' '.join([key, '重要度', weight, '%'])
        ])

        for r in results:
            r["point"] += calc_weight(r["model"], weight)

    # あいまい検索
    for ambiguous_item in list(filter(lambda x: x.ambiguous, searchs)):
        ambiguous_item_name = ambiguous_item.name

        # search_consitions の中から対象とするあいまい検索の項目を取り出す
        key = find_in_double_list(ambiguous_item_name, search_conditions)

        # 検索項目に含まれない場合はスキップ
        if not key:
            continue

        # 検索タイプで計算方法を変える（プルダウンのみ考える TODO: 別の検索タイプにも対応？？）
        search_type = get_search_type(key)

        # プルダウン
        if (search_type == 2):

            # 正規分布の計算に必要な値を取得
            search = Search.query.filter(Search.name == key)
            min = search.search_min
            max = search.search_max
            step = search.step
            pull_menu_num = get_pull_menu_num(min, max, step)

            for r in results:
                r["point"] += calc_ambigious_pull(key, r["model"], pull_menu_num)

    # 点数の高い順に上から表示できるようにsort
    results = sorted(results, key=lambda x: x["point"], reverse=True)

    # ポイントの規格化（最大は100にする）
    results = normalize_point(results)

    return render_template(
        "search/index.html",
        results=results,
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
def find_in_double_list(i, l):
    return next(filter(lambda x: x[0] == i, l), None)


def get_search_type(key):
    return Search.query.filter(Search.name_en == key).all()[0].search_type


def get_pull_menu_num(min, max, step):
    return math.ceil((max - min)/step + 1)


# 重要度検索
def calc_weight(weight):
    point = 1
    return point * int(weight)/100


# 正規分布を用いてあいまい検索を行う
def calc_ambigious_pull(key, model, num):
    point = 1

    # TODO：正規分布に当てはめて、補正係数を取得
    # ave = 

    corr_coef = 1

    return point * corr_coef


def normalize_point(hash):
    return hash


# Searchモデルから検索条件の一覧を取得
def get_searchs():
    searchs = Search.query.all()

    for search in searchs:

        # チェックボックス
        if search.search_type == 1:

            # 検索項目に該当するデータを全て取得→チェックボックスで全て表示できるように
            items = []
            results = Home.query.distinct(eval('Home.' + search.name_en)).all()

            for result in results:
                items.append(eval('result.' + search.name_en))

            search.items = ",".join(items)

        # プルダウン
        elif search.search_type == 2:

            # 該当プロパティのmax・minを取得
            results = Home.query.order_by(eval('Home.' + search.name_en)).distinct(eval('Home.' + search.name_en)).all()

            min = eval('results[0].' + search.name_en)
            max = eval('results[-1].' + search.name_en)

            step = search.step

            # プルダウンのアイテム数を計算
            search.pull_menu_num = get_pull_menu_num(min, max, step)

            # 表示させるのに最適な値に丸める
            search.search_min = math.ceil(min/step - 1) * step
            search.search_max = math.ceil(max/step) * step

            # TODO: 万、億などの桁を丸める

    searchs = sorted(searchs, key=lambda x: x.search_order)

    return searchs


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
