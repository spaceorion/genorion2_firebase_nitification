web: gunicorn myproject.wsgi
celery -A myproject beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A myproject worker -l INFO
web: daphne myproject.asgi:application --port $PORT --bind 0.0.0.0 -v2
####git commit -m "first commit"  git push -u origin123 main