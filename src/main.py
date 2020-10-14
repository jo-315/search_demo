from flask import render_template, request
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
    homes = []
    # 確定検索
    name = request.form.get('name')
    address = request.form.get('address')
    if len(name) != 0:
        homes = Home.query.filter_by(name=name).all()
    elif len(address) != 0:
        homes = Home.query.filter_by(address=address).all()
    result_num = len(homes)

    # あいまい検索
    return render_template("index.html", homes=homes, result_num=result_num)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
