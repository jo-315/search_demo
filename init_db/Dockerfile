FROM postgres:13.0

# RUN mkdir /search_demo
# WORKDIR /search_demo

# ADD . /search_demo
COPY ./*.sql /docker-entrypoint-initdb.d/

# CMD ./init_db.sh