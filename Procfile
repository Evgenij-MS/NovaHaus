# Замените содержимое на:
release: python manage.py migrate
web: gunicorn NovaHaus.wsgi --workers=2 --threads=4 --worker-class=gthread --bind=0.0.0.0:$PORT
