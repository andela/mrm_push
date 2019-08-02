import os
from celery import Celery
from app import create_app
from datetime import timedelta
from celery.schedules import crontab


app = create_app(os.getenv('APP_SETTINGS') or 'default')


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL=app.config['REDIS_DATABASE_URI']
)
celery = make_celery(app)

celery.conf.beat_schedule = {
    'add-every-one-minute': {
        'task': 'push_notification.refresh',
        'schedule': crontab(minute=0, hour=0, day_of_week='sunday'),
    },
    'schedule-create-channels': {
        'task': 'push_notification.add-channels',
        'schedule': crontab(minute=0, hour=0, day_of_week='sunday'),
    },
}
celery.conf.timezone = 'UTC'
