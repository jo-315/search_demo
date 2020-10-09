#!/bin/sh

pip install -r ./requirements.txt
# flask run -h 0.0.0.0 -p 5000
flask run -h 0.0.0.0 -p $PORT