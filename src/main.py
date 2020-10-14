from flask import render_template, request
from src import app
from src.models import Home


@app.route('/', methods=['GET'])
def index():
    homes = Home.query.all()
    result_num = len(homes)
    return render_template("index.html", homes=homes, result_num=result_num)


@app.route('/search', methods=['POST'])
def post():
    name = request.form.get('name')
    address = request.form.get('address')
    if len(name) != 0:
        homes = Home.query.filter_by(name=name)
    elif len(address) != 0:
        homes = Home.query.filter_by(address=address)
    result_num = homes.count()
    return render_template("index.html", homes=homes, result_num=result_num)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
