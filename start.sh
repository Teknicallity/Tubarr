#!/bin/bash

TB_SERVER_PORT="${TB_SERVER_PORT:-3020}"

mkdir -p media

#python manage.py generate_secret_key

#python manage.py create_initial_superuser

python3 manage.py migrate

if [ "$DISABLE_BACKGROUND_TASKS" != "True" ]; then
  supervisord -c supervisord.conf
fi

python3 manage.py runserver "0.0.0.0:${TB_SERVER_PORT}"
