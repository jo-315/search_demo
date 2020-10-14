from flask import render_template, request
from src import app
from src.models import Home


@app.route('/', methods=['GET'])
def index():
    homes = Home.query.all()
    return render_template("index.html", homes=homes)


@app.route('/search', methods=['POST'])
def post():
    name = request.form.get('name')
    address = request.form.get('address')
    if len(name) != 0:
        homes = Home.query.filter_by(name=name)
    elif len(address) != 0:
        homes = Home.query.filter_by(address=address)
    return render_template("index.html", homes=homes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
