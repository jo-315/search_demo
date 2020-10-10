FROM postgres

# COPY ./init_db/init_db.sh .
COPY ./docker-entrypoint-initdb.d/*.sql /docker-entrypoint-initdb.d/
# COPY ./init_db/docker-entrypoint-initdb.d/*.sql /docker-entrypoint-initdb.d/

# CMD ./init_db.sh