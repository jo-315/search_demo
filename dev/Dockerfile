# python3.7のイメージ構築
FROM python:3.7

# 作業用ディレクトリの作成
RUN mkdir /code
WORKDIR /code

# appをマウントする
ADD ./app /code

# pythonパッケージのインストール
RUN pip install -r requirements.txt