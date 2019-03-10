"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import pathlib
import datetime
from envparse import env

env.read_envfile()

# Base path
BASE_PATH = pathlib.Path(__file__).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

SECRET_KEY = env('SECRET_KEY', cast=str, default='f)x_76pg46@omifv%=f0evs(4fiqkbr_k1p%nld2qtey8dyoc(')

DEBUG = env('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_celery_beat',
    'django_celery_results',
    'django_celery_monitor',
    'raven.contrib.django.raven_compat',
    'jsoneditor',
]

LOCAL_APPS = [
    'apps.bpc',
    'apps.fcmoto',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB_NAME', default=''),
        'USER': env('POSTGRES_DB_USER', default=''),
        'PASSWORD': env('POSTGRES_DB_PASSWORD', default=''),
        'HOST': env('POSTGRES_DB_HOST', default=''),
        'PORT': env('POSTGRES_DB_PORT', default=''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_PATH / 'static'

# Media files (Images, Video, pdf, etc)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_PATH / 'media'

# Data upload
DATA_UPLOAD_MAX_NUMBER_FIELDS = 25000
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 4

### Celery
# General settings
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ENABLE_UTC = False

# Task settings
CELERY_TASK_ANNOTATIONS = {'*': {'rate_limit': '10/s'}}
CELERY_TASK_COMPRESSION = 'gzip'
CELERY_TASK_PROTOCOL = 2
CELERY_task_serializer = 'json'
CELERY_task_publish_retry = True
CELERY_task_publish_retry_policy = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

# Task execution settings
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False
CELERY_TASK_REMOTE_TRACEBACKS = False
CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_STORE_ERRORS_EVEN_IF_IGNORED = False
CELERY_TASK_TRACK_STARTED = False
CELERY_TASK_TIME_LIMIT = int(datetime.timedelta(days=1).total_seconds())
# CELERY_TASK_SOFT_TIME_LIMIT = None
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = False
# CELERY_TASK_DEFAULT_RATE_LIMIT = '1000/m'

# Task result backend settings
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', cast=str, default='django-db')  # django-db | redis://localhost
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {'visibility_timeout': 18000}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_COMPRESSION = 'gzip'
CELERY_RESULT_EXPIRES = int(datetime.timedelta(days=1).total_seconds())
CELERY_RESULT_CACHE_MAX = False

# Redis backend setting
CELERY_REDIS_BACKEND_USE_SSL = False
# CELERY_REDIS_MAX_CONNECTIONS = None
# CELERY_REDIS_SOCKET_CONNECT_TIMEOUT = None
CELERY_REDIS_SOCKET_TIMEOUT = 120.0

# Message Routing
from kombu import Queue, Exchange
# CELERY_TASK_QUEUES = {
#     Queue(name='celery', exchange=Exchange('celery'), routing_key='celery.#', durable=True),
#     Queue(name='high', exchange=Exchange('high'), routing_key='high.#', durable=True),
#     Queue(name='normal', exchange=Exchange('normal'), routing_key='normal.#', durable=True),
#     Queue(name='low', exchange=Exchange('low'), routing_key='low.#', durable=True),
# }
CELERY_TASK_ROUTES = (
    {
        'apps.fcmoto.tasks.category.category_task': {'queue': 'fcmoto_category'},
        'apps.fcmoto.tasks.product.product_task': {'queue': 'fcmoto_product'},
        'apps.fcmoto.tasks.page.page_task': {'queue': 'fcmoto_page'},
    }
)
CELERY_TASK_QUEUE_HA_POLICY = {'all'}  # RabbitMQ
CELERY_TASK_QUEUE_MAX_PRIORITY = None  # RabbitMQ
# CELERY_WORKER_DIRECT = False
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_TASK_DEFAULT_QUEUE = 'celery'
CELERY_TASK_DEFAULT_EXCHANGE = 'celery'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'celery'
CELERY_TASK_DEFAULT_DELIVERY_MODE = 'persistent'

# Broker settings
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='amqp://')
# CELERY_BROKER_READ_URL = 'amqp://user:pass@broker.example.com:56721'
# CELERY_BROKER_WRITE_URL = 'amqp://user:pass@broker.example.com:56722'
CELERY_BROKER_FAILOVER_STRATEGY = 'round-robin'
CELERY_BROKER_HEARTBEAT = 120.0
CELERY_BROKER_HEARTBEAT_CHECKRATE = 2.0
# CELERY_BROKER_USE_SSL = {
#   'keyfile': '/var/ssl/private/worker-key.pem',
#   'certfile': '/var/ssl/amqp-server-cert.pem',
#   'ca_certs': '/var/ssl/myca.pem',
#   'cert_reqs': ssl.CERT_REQUIRED
# }
CELERY_BROKER_POOL_LIMIT = 20
CELERY_BROKER_CONNECTION_TIMEOUT = 4.0
CELERY_BROKER_CONNECTION_MAX_RETRIES = 100
CELERY_BROKER_LOGIN_METHOD = 'AMQPLAIN'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 18000}

# Worker
CELERY_IMPORTS = []
CELERY_INCLUDE = []
# CELERY_WORKER_CONCURRENCY = 4 # Default: Number of CPU cores.
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_LOST_WAIT = 10.0
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1  # Default: no limit
CELERY_WORKER_MAX_MEMORY_PER_CHILD = 120000  # Default: no limit
CELERY_WORKER_DISABLE_RATE_LIMITS = False
CELERY_WORKER_STATE_DB = None
CELERY_WORKER_TIMER_PRECISION = 1.0
CELERY_WORKER_ENABLE_REMOTE_CONTROL = True

# Event
CELERY_WORKER_SEND_TASK_EVENTS = False
CELERY_TASK_SEND_SENT_EVENT = False
CELERY_EVENT_QUEUE_TTL = 5.0  # amqp
CELERY_EVENT_QUEUE_EXPIRES = 60.0  # amqp
CELERY_EVENT_QUEUE_PREFIX = 'celeryev'
CELERY_EVENT_SERIALIZER = 'json'

# Remote Control Commands
CELERY_CONTROL_QUEUE_TTL = 300.0
CELERY_CONTROL_QUEUE_EXPIRES = 10.0

# Celery logging
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_LOG_COLOR = True
CELERY_WORKER_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
CELERY_WORKER_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s'
CELERY_WORKER_REDIRECT_STDOUTS = True
CELERY_WORKER_REDIRECT_STDOUTS_LEVEL = 'DEBUG'

# Security
CELERY_SECURITY_KEY = None
CELERY_SECURITY_CERTIFICATE = None
CELERY_SECURITY_CERT_STORE = None

# Custom Component Classes (advanced)
# CELERY_WORKER_POOL = 'prefork'
# CELERY_WORKER_POOL_RESTARTS = True
# CELERY_WORKER_AUTOSCALER = 'celery.worker.autoscale:Autoscaler'
# CELERY_WORKER_CONSUMER = 'celery.worker.consumer:Consumer'
# CELERY_WORKER_TIMER = 'kombu.asynchronous.hub.timer:Timer'

# Beat Settings (celery beat)
CELERY_BEAT_SCHEDULE = {}
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE_FILENAME = 'celerybeat-schedule'
CELERY_BEAT_SYNC_EVERY = 0
CELERY_BEAT_MAX_LOOP_INTERVAL = 300

### Application logging
import raven
LOG_LEVEL = env('LOG_LEVEL', cast=str, default='INFO').upper()
RAVEN_DSN = env.str('RAVEN_DSN', default='')
RAVEN_CONFIG = {
    'dsn': RAVEN_DSN,
    'release': raven.fetch_git_sha(BASE_PATH),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'syslog': {
            'format': '%(levelname)s <PID %(process)d> '
                      '%(name)s.%(funcName)s(): %(message)s'
        },
        'verbose': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(levelname) -10s %(asctime)s '
                      '%(processName) -35s %(name) -35s '
                      '%(funcName) -30s %(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'apps.bpc': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'apps.fcmoto': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}

# Selenoid
SELENOID_HUB = env('SELENOID_HUB', cast=str, default='http://selenoid:4444/wd/hub')
