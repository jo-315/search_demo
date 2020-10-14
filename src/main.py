from flask import render_template, request
from src import app
# import models
from src.models import Home


@app.route('/', methods=['GET'])
def index():
    homes = Home.query.all()
    return render_template("index.html", homes=homes)


@app.route('/search', methods=['POST'])
def post():
    name = request.form.get('name')
    home = Home.query.filter_by(name=name).first()
    return render_template("index.html", homes=[home])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="PORT", debug=True)
