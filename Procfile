web: gunicorn kmcoffice.wsgi --log-file -
worker: celery -A kmcoffice worker -l info
beat: celery -A kmcoffice beat -l info