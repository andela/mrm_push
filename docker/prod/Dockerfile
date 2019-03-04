
FROM python:3.6

WORKDIR /app

RUN apt-get update -u

COPY . /app

RUN pip install -r requirements.txt && \
        pip install sqlalchemy && \
        pip install gunicorn && \
        pip install gevent
