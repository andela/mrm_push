
FROM python:3.6

WORKDIR /app

RUN apt-get update -u && apt-get install -y \
        supervisor

COPY docker/prod/push_service.conf /etc/supervisor/conf.d/push_service.conf

COPY . /app

RUN pip install -r requirements.txt && \
        pip install sqlalchemy && \
        pip install gunicorn && \
        pip install gevent
