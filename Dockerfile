# python3.7のイメージ構築
FROM python:3.7

# 作業用ディレクトリの作成
RUN mkdir /app
WORKDIR /app

# appをマウントする
ADD . /app

ENV FLASK_APP=./src/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=$FLASK_ENV
ENV PORT=$PORT

CMD PORT=${PORT} ./flask.sh
