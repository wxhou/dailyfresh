"""
WSGI config for dailyfresh project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = os.environ.get('DAILYFRESH')
if env is None:
    raise EnvironmentError("环境变量`DAILYFRESH`未设置！")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'dailyfresh.settings.{env}')

application = get_wsgi_application()
