#!/bin/bash
export DJANGO_SETTINGS_MODULE=DomePortfolio.settings.production

command="poetry run python <<< 'from django.conf import settings; print(settings.CLOUD_SQL_CONN_NAME)'"
eval "$command" > ./test.log
conn_string=$(cat ./test.log)
rm -rf ./test.log

~/cloud_sql_proxy -instances="$conn_string"=tcp:5432 &
pid=$!

poetry run python manage.py migrate --no-input
poetry run python manage.py collectstatic --no-input

gcloud app deploy

rm -rf static
kill %"$pid"
exit 0
