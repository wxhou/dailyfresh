from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

env = os.environ.get('DAILYFRESH')
if env is None:
    raise EnvironmentError("环境变量`DAILYFRESH`未设置！")

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'dailyfresh.settings.{env}')

app = Celery('dailyfresh')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def main():
    pass


if __name__ == '_main__':
    main()
