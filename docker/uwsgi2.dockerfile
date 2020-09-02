FROM tiangolo/uwsgi-nginx:python3.8

ENV UWSGI_INI /application/uwsgi.ini

RUN apt-get update
RUN apt-get install -y curl gcc build-essential python-dev

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

ENV DJANGO_SETTINGS_MODULE DomePortfolio.settings.development

WORKDIR /application/

RUN python manage.py migrate && python manage.py collectstatic

ENV LISTEN_PORT 8080
EXPOSE 8080
