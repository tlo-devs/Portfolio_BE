#!/bin/bash
set -eu

# In case we are running on Google Cloud Run, overwrite the config value
port=${PORT:-"$NGINX_PORT"}

export NGINX_PORT=${port:-8080}
export NGINX_HOST=${NGINX_HOST:-localhost}
export STATS_PORT=${STATS_PORT:-1717}

# shellcheck disable=SC2016
envsubst '${NGINX_PORT} ${NGINX_HOST} ${STATS_PORT}' \
  < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# Own the application and static directories as well as the uwsgi.ini file to the nginx group
# This way both nginx and uwsgi can access the applications files
locations=("/application" "/var/django/projects/DomePortfolio/static" "/uwsgi.ini")

for location in "${locations[@]}"; do
  chmod -R 770 "$location"
  chown -R root:nginx "$location"
done

# Configure user and group for uwsgi to run on
uwsgi_user="uwsgi-django"
useradd -G nginx --system --no-create-home "$uwsgi_user"

# Start the prometheus node exporter
"/opt/node_exporter-1.0.1.linux-amd64/node_exporter" &

uwsgi --uid "$(id -u $uwsgi_user)" --gid "$(id -g $uwsgi_user)" --ini "/uwsgi.ini" &

# Start the prometheus uwsgi exporter
"/opt/uwsgi_exporter" --stats.uri "http://127.0.0.1:1919" --web.listen-address ":9117" &

exec "$@"
