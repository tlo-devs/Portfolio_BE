FROM tiangolo/uwsgi-nginx:python3.8

RUN apt-get update && apt-get install -y curl ca-certificates mime-support

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /application/
COPY ["pyproject.toml", "poetry.lock", "manage.py", "server/uwsgi.ini", "./"]
RUN poetry install --no-root --no-dev

WORKDIR /application/keys/
COPY ["keys", "./"]

WORKDIR /application/DomePortfolio/
COPY ["DomePortfolio", "./"]

WORKDIR /application/

ENV UWSGI_INI /application/uwsgi.ini
ENV DJANGO_SETTINGS_MODULE DomePortfolio.settings.development

RUN python manage.py migrate && python manage.py collectstatic
COPY ["server/custom.conf", "/etc/nginx/conf.d/"]

ENV LISTEN_PORT 8080
EXPOSE 8080
