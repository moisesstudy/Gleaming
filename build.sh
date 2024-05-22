#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install

# se realizara el comando collectstatic en la nube
python manage.py collectstatic --no-input

# para genrar las tablas de labase de datos - postgreSQL
python manage.py migrate
