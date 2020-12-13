import math
from scipy.stats import norm
from statistics import stdev
import re
from flask import render_template, request
from sqlalchemy import and_
from src import app
from src.models import Model, Search

# 最初の検索画面
@app.route('/', methods=['GET'])
def index():
    # モデルの総数
    results = Model.query.all()
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
    # {key(日本語): value1（検索項目）, value2(重要度)}
    search_conditions = []

    # 検索条件をparamsに格納
    params = []

    # 重要度を格納
    # [[key_en1, value1], ...]
    weights = []

    # もし名前で検索されていたらここに名前を入れる
    name = None

    # 検索された項目をフロントエンドから取得
    request_items = request.form.to_dict(flat=False)

    for key_en in request_items.keys():
        # 重要度の場合
        if(re.search('.*_weight', key_en)):
            weights.append([key_en, request_items[key_en][0]])

        # 検索条件の場合
        else:
            # チェックボックスで複数の条件を指定した場合
            if (len(request_items[key_en]) > 1):

                # 複数の値を取得するために `request_items` を使う
                values = request_items[key_en]

                search_conditions.append([
                    get_search_conditions_key_name(searchs, key_en),
                    ' '.join(values)
                    ])

                params.append(eval('Model.' + key_en + '.in_(' + str(values) + ')'))

            # 指定した条件が一つ
            else:

                value = request_items[key_en][0]

                # 検索が行われなかった場合
                if (value == 'null' or len(value) == 0):
                    continue

                # 名前で検索が行われている場合
                if (key_en == 'name'):
                    name = value

                # 検索タイプで分岐処理
                search_type = get_search_type(key_en)

                # テキスト or チェックボックス
                if (search_type == 0 or search_type == 1):
                    # queryに利用
                    params.append(eval('Model.' + key_en + '==' + value + ')'))

                    # フロントで表示用の配列にappend
                    search_conditions.append([
                        get_search_conditions_key_name(searchs, key_en),
                        value
                    ])

                # プルダウン
                elif (search_type == 2):
                    # フロントで表示用に指定範囲を取得
                    search_conditions_key_name = get_search_conditions_key_name(searchs, key_en)
                    search = Search.query.filter(Search.name_en == key_en).all()[0]
                    value = str(int(search.search_min) + int(search.step) * int(value)) \
                        + '~' \
                        + str(int(search.search_min) + int(search.step) * (int(value)+1)) \
                        + search.unit
                    search_conditions.append([search_conditions_key_name, value])

    # 実際に検索を行う
    results = Model.query.filter(
        and_(
            Model.name == name if name else True,
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
    results = [{"model": result, "point": 0, "tmp": -1} for (result) in results]

    # 重要度の計算
    for weight_item in list(filter(lambda x: x.weight, searchs)):
        weight_item_name = weight_item.name
        weight_item_name_en = weight_item.name_en

        # 検索項目に含まれない場合はスキップ(search_consitions の中に格納されているかどうか)
        key_list = find_in_double_list(weight_item_name, search_conditions)
        if not key_list:
            continue

        weight_item = find_in_double_list(weight_item_name_en + '_weight', weights)
        weight = weight_item[1]

        # search_conditionsに重要度を格納
        list(filter(lambda x: x[0] == weight_item_name, search_conditions))[0].append(' '.join(['重要度', weight, '%']))

        # あいまい検索のために一度tmpに格納
        for r in results:
            r["tmp"] = calc_weight(weight)

    # あいまい検索
    for ambiguous_item in list(filter(lambda x: x.ambiguous, searchs)):
        ambiguous_item_name = ambiguous_item.name
        ambiguous_item_name_en = ambiguous_item.name_en

        # 検索項目に含まれない場合はスキップ
        key_list = find_in_double_list(ambiguous_item_name, search_conditions)
        if not key_list:
            continue

        # 検索タイプで計算方法を変える（プルダウンのみ考える TODO: 別の検索タイプにも対応？？）
        search_type = get_search_type(ambiguous_item_name_en)

        # プルダウン
        if (search_type == 2):

            # 正規分布の計算に必要な値を取得
            search = Search.query.filter(Search.name == key_list[0]).all()[0]
            min = search.search_min
            max = search.search_max
            step = search.step

            # 標準偏差の計算
            pull_menu_num = get_pull_menu_num(min, max, step)
            seq = range(pull_menu_num)
            scale = stdev(seq)

            # 検索された項目を取得（正規分布の平均にする）
            loc = float(request.form[ambiguous_item.name_en])

            for r in results:
                if r["tmp"] < 0:
                    point = 1
                else:
                    point = r["tmp"]
                    r["tmp"] = -1

                # モデルの持つ該当データの値を取得
                x = (eval("r['model']" + '.' + eval("ambiguous_item_name_en")) - min) / step

                r["point"] += calc_ambigious_pull(x, loc, scale, point)

    # 重要度検索をしたがあいまい検索はしなかった場合
    for r in results:
        if r["tmp"] > 0:
            r["point"] += r["tmp"]

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


def get_search_conditions_key_name(searchs, key_en):
    return list(filter(lambda x: x.name_en == key_en, searchs))[0].name


# 重要度検索
def calc_weight(weight):
    point = 1
    return point * int(weight)/100


# 正規分布を用いてあいまい検索を行う
def calc_ambigious_pull(x, loc, scale, point):

    # 正規分布に当てはめて、補正係数を取得
    corr_coef = norm.pdf(x=x, loc=loc, scale=scale)

    return point * corr_coef


def normalize_point(hash):
    max_point = hash[0]["point"]

    # あいまい検索が行われなかった場合は、全てのポイントが0なので代わりに100を代入する
    if max_point == 0:
        for h in hash:
            h["point"] = 100
    else:
        for h in hash:
            # 規格化
            h["point"] = round(h["point"] / max_point * 100)

    return hash


# Searchモデルから検索条件の一覧を取得
def get_searchs():
    searchs = Search.query.all()

    for search in searchs:

        # チェックボックス
        if search.search_type == 1:

            # 検索項目に該当するデータを全て取得→チェックボックスで全て表示できるように
            items = []
            results = Model.query.distinct(eval('Model.' + search.name_en)).all()

            for result in results:
                items.append(eval('result.' + search.name_en))

            search.items = ",".join(items)

        # プルダウン
        elif search.search_type == 2:

            # 該当プロパティのmax・minを取得
            results = Model.query.order_by(eval('Model.' + search.name_en)).distinct(eval('Model.' + search.name_en)).all()

            min = eval('results[0].' + search.name_en)
            max = eval('results[-1].' + search.name_en)

            step = search.step

            # プルダウンのアイテム数を計算
            search.pull_menu_num = get_pull_menu_num(min, max, step)

            # 表示させるのに最適な値に丸める
            search.search_min = math.floor(min/step) * step
            search.search_max = math.ceil(max/step) * step

            # TODO: 万、億などの桁を丸める

    searchs = sorted(searchs, key=lambda x: x.search_order)

    return searchs


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
