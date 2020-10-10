#!/bin/sh

pip install -r ./requirements.txt

flask db init
flask db migrate
flask db upgrade

heroku pg:psql postgresql-contoured-15367 --app search-demo-1234 --file ./init_db/init.sql

flask run -h 0.0.0.0 -p $PORT