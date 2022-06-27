#dailyfresh


### 启动项目

```shell
python manage.py runserver 8000
```

### 启动celery

```shell
celery -A dailyfresh.celery worker -l info -P eventlet -c 1000
```