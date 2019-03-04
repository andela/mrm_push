from config import config

import os
import sys
import redis
sys.path.append(os.getcwd())

config_name = os.getenv('APP_SETTINGS')
database_uri = config.get(config_name).REDIS_DATABASE_URI
db = redis.from_url(database_uri, charset="utf-8", decode_responses=True)
