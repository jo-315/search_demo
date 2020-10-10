#!/bin/sh

psql -U postgres --file /docker-entrypoint-initdb.d/init.sql