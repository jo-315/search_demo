FROM python:3.7

RUN mkdir /app
WORKDIR /app

ADD . /app

ENV FLASK_APP=./src/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=$FLASK_ENV
ENV PORT=$PORT

CMD PORT=${PORT} ./flask.sh
