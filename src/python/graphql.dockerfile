FROM python:3.9.5-slim-buster as python-base

RUN mkdir /flask
WORKDIR /flask/

RUN apt-get update
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml /flask
RUN poetry install --no-root --no-dev

COPY . /flask

RUN poetry install --no-dev
WORKDIR /imdb_graphql/
EXPOSE 5000
