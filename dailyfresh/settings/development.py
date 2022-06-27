"""
Django settings for dailyfresh project.

Generated by 'django-admin startproject' using Django 2.2.22.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from datetime import timedelta
from django.conf.global_settings import gettext_noop
from typing import List, Tuple

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_BASE_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, os.path.join(ROOT_BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2p-)s47f#3^!h11g4^+ar7$9m_0nv^5tw02$sv#gvxx63zhn-a'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_yasg',  # swagger
    'django_celery_results',  # celery结果后端
    'corsheaders',
    'django_minio_backend',
    'ckeditor',
    'ckeditor_uploader',
    'apps.user',
    'apps.goods',
    'apps.shop'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dailyfresh.urls'

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
        'HOST': '127.0.0.1',  # 服务IP
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

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# email
EMAIL_HOST = 'smtp.126.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'twxhou@126.com'
EMAIL_HOST_PASSWORD = 'GQWJDUKVWNOJLPOH'

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

WSGI_APPLICATION = 'dailyfresh.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

# DATE_TIME takes effect, since the localization of l10n overrides DATETIME_FORMAT and DATE_FORMAT as documented at: https://docs.djangoproject.com/en/1.9/ref/settings/#date-format
USE_L10N = True

# USE_TZ = True  # 默认是Ture，时间是utc时间，如要用本地时间，所用手动修改为false！！！！
USE_TZ = False

LANGUAGES = (
    ('zh-hans', gettext_noop('Simplified Chinese')),
)

# 翻译文件所在目录，需要手工创建
LOCALE_PATHS = (
    os.path.join(ROOT_BASE_DIR, 'locale'),
)

# 自定义登录
AUTH_USER_MODEL = 'user.User'
# User Register Confirm Timedelta
REGISTER_CONFIRM_TIMEDELTA = 30

AUTHENTICATION_BACKENDS = (
    'apps.user.backends.CustomBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# 静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(ROOT_BASE_DIR, 'static'),)

# 上传文件
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_BASE_DIR, 'media')
CKEDITOR_UPLOAD_PATH = 'ckeditor/'

# Celery消息队列
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'redis'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# rest_framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated core.
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATETIME_INPUT_FORMATS': '%Y-%m-%d',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'common.paginations.StandardPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'EXCEPTION_HANDLER': 'common.exceptions.my_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# SWAGGER    drf-swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'}
    },
    'LOGIN_URL': '/api-auth/login/',
    'LOGOUT_URL': '/api-auth/logout/',
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}

# 日志系统
LOG_FILE_DEBUG = os.path.join(ROOT_BASE_DIR, 'logs', 'debug.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
                '%(levelname)s %(asctime)s '
                '[%(filename)s.%(funcName)s:%(lineno)s] '
                '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s  %(message)s '
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },

        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_true']
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_DEBUG,
            'mode': 'a',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'root': {
            'level': 'WARNING',
            'handlers': ['null'],
        },
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'debug': {
            'handlers': ['console', 'debug', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'
MINIO_ENDPOINT = '127.0.0.1:9000'
MINIO_ACCESS_KEY = 'wxhou'
MINIO_SECRET_KEY = 'hoou1993'
MINIO_USE_HTTPS = False
MINIO_URL_EXPIRY_HOURS = timedelta(days=1)  # Default is 7 days (longest) if not defined
MINIO_CONSISTENCY_CHECK_ON_START = True
MINIO_PRIVATE_BUCKETS = [
    'dailyfresh-media-bucket'
]
MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = []
MINIO_MEDIA_FILES_BUCKET = 'dailyfresh-media-bucket'  # replacement for MEDIA_ROOT
MINIO_BUCKET_CHECK_ON_SAVE = False  # Default: True // Creates bucket if missing, then save

if __name__ == '__main__':
    print(BASE_DIR)
