web: gunicorn ghmonitor.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=ghmonitor --loglevel=info
