import os
from celery import Celery
from app import create_app
from datetime import timedelta
from celery.schedules import crontab


app = create_app(os.getenv('APP_SETTINGS') or 'default')

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
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
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
    )
celery = make_celery(app)

@celery.task(name='cworker.add_together')
def add_together(a, b):
    return a + b

result = add_together.delay(23, 42)


celery.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'app.see_you',
        'schedule': 5.0,
        'args': ()
    },
}
celery.conf.timezone = 'UTC'