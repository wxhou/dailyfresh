from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "drf_dailyfresh",
        'USER': 'root',  # 用户名，可以自己创建用户
        'PASSWORD': 'root1234',  # 密码
        'HOST': '192.168.0.163',  # 服务IP
        'PORT': '3306',  # 端口
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# email
EMAIL_HOST = 'smtp.126.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'twxhou@126.com'
EMAIL_HOST_PASSWORD = 'GQWJDUKVWNOJLPOH'

# celery
# Celery消息队列
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'redis'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
