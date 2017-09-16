web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn kmcoffice.wsgi --log-file -
worker: celery -A kmcoffice worker -B -l info