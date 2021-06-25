# coding: utf-8

from .base import *
from libs.config import Config
from libs.django.middleware.log import get_log_config

CONFIG_INFO = Config(os.path.join(BASE_DIR, '.env')).format()

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'app_user',
    'app_mall',
]

MIDDLEWARE += [
    'libs.django.middleware.log.RequestLogMiddleware'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CONFIG_INFO['db']['schema'],
        'HOST': CONFIG_INFO['db']['host'],
        'PORT': CONFIG_INFO['db']['port'],
        'USER': CONFIG_INFO['db']['user'],
        'PASSWORD': CONFIG_INFO['db']['password'],
        'CONN_MAX_AGE': int(CONFIG_INFO['db']['conn_max_age']),
        'OPTIONS': {
            'charset': CONFIG_INFO['db']['charset'],
            'init_command': 'set session transaction_isolation = "READ-COMMITTED"'
        }
    }
}

LOGGING = get_log_config(BASE_DIR, is_pro=True)
