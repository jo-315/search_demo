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
    layout = request.form.get('layout')
    structure = request.form.get('structure')
    homes = Home.query.filter(
        or_(
            Home.name == name,
            and_(
                Home.address == address if address else True,
                Home.layout == layout if layout else True,
                Home.structure == structure if structure else True
            )
        )
    ).all()
    result_num = len(homes)

    # あいまい検索 TODO
    return render_template("index.html", homes=homes, result_num=result_num)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
