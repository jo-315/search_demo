from flask import render_template, request
from app import app
# import models
from app.models import Home


@app.route('/')
def index():
    homes = Home.query.all()
    return render_template("index.html", homes=homes)


@app.route('/', methods=['POST'])
def post():
    name = request.form.get('name')
    home = Home.query.filter_by(name=name)
    return render_template("index.html", homes=[home])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
