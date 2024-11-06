#!/bin/bash

TB_SERVER_PORT="${TB_SERVER_PORT:-3020}"

mkdir -p /etc/tubarr/media
mkdir -p /etc/tubarr/config
chown -R www-data: /etc/tubarr/config

chown www-data: /etc/tubarr

#python manage.py generate_secret_key

#python manage.py create_initial_superuser

python3 manage.py migrate

exec uwsgi --http :"$TB_SERVER_PORT" --ini uwsgi.ini
