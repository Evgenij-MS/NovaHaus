web: gunicorn NovaHaus.wsgi --workers=3 --threads=2 --worker-class=gthread --max-requests=1000 --max-requests-jitter=50 --timeout=30 --bind=0.0.0.0:$PORT
release: python manage.py migrate