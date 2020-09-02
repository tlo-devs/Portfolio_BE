FROM python:3.8.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y curl gcc build-essential python-dev

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /application/

COPY ["pyproject.toml", "poetry.lock", "manage.py", "./"]

RUN poetry install --no-root --no-dev
RUN poetry add uwsgi

WORKDIR /application/keys/

COPY ["keys", "./"]

WORKDIR /application/DomePortfolio/

COPY ["DomePortfolio", "./"]

ENV DJANGO_SETTINGS_MODULE DomePortfolio.settings.development

WORKDIR /application/

RUN python manage.py migrate && python manage.py collectstatic

WORKDIR /
COPY ["./server/uwsgi.ini", "./"]

EXPOSE 3031
CMD ["uwsgi", "uwsgi.ini"]
