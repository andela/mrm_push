import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hardtoguessstring'
    REDIS_DATABASE_URI = os.getenv('DEV_REDIS_URL')
    REDIS_DATABASE_URI = os.getenv('PROD_REDIS_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    NOTIFICATION_URL = os.getenv('DEV_NOTIFICATION_URL')
    CONVERGE_MRM_URL = os.getenv('DEV_CONVERGE_MRM_URL')
    REDIS_DATABASE_URI = os.getenv('DEV_REDIS_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')


class ProductionConfig(Config):
    NOTIFICATION_URL = os.getenv('NOTIFICATION_URL')
    CONVERGE_MRM_URL = os.getenv('CONVERGE_MRM_URL')
    REDIS_DATABASE_URI = os.getenv('PROD_REDIS_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

class TestingConfig(Config):
    DEBUG = True
    NOTIFICATION_URL = os.getenv('DEV_NOTIFICATION_URL')
    CONVERGE_MRM_URL = os.getenv('DEV_CONVERGE_MRM_URL')
    REDIS_DATABASE_URI = os.getenv('TEST_REDIS_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig
}
