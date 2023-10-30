# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10
FROM python:3.10-slim-bookworm as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
USER root

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./requirements.txt,target=/app/requirements.txt \
    python -m pip install -r requirements.txt

COPY ./ /app

RUN mkdir /app/static
RUN chmod -R -770 /app
RUN chmod -R -777 /app/static

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=0
ENV PYTHONUNBUFFERED=0

CMD python manage.py makemigrations data_viewer && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn --timeout 500 --bind 0.0.0.0:8000 headstart_status_viewer.wsgi:application