from flask import render_template
from app import app
# from models import Home


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
