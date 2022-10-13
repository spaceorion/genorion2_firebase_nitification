release:python3 manage.py worker
web:gunicorn myproject.wsgi
web:daphne myproject.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker:python manage.py runworker -v2