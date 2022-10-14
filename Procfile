web: gunicorn myproject.wsgi
celery -A myproject beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A myproject worker -l INFO
####git commit -m "first commit"