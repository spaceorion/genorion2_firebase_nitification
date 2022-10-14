web: gunicorn myproject.wsgi
celery: celery -A myproject worker -l INFO
celery: celery -A myproject beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
#web: daphne myproject.asgi:application --port $PORT --bind 0.0.0.0 -v2
####git commit -m "first commit"  git push -u origin123 main
