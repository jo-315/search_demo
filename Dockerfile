# python3.7のイメージ構築
FROM python:3.7

# 作業用ディレクトリの作成
RUN mkdir /app
WORKDIR /app

# appをマウントする
ADD . /app

ENV FLASK_APP ./src/main.py

CMD flask run -h 0.0.0.0 -p $PORT
