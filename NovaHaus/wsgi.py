
"""
WSGI config for NovaHaus project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os
import sys
import logging
from django.core.wsgi import get_wsgi_application

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Django Settings Modul setzen
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NovaHaus.settings')

try:
    # WSGI Application erstellen
    application = get_wsgi_application()
    logger.info("Django WSGI application successfully initialized")
except Exception as e:
    logger.error(f"Failed to initialize Django WSGI application: {e}")
    # Fallback für kritische Fehler
    sys.exit(1)

# Für Produktionsumgebungen: SSL und Security Headers
def application_with_security(environ, start_response):
    """
    Wrapper für zusätzliche Sicherheitsmaßnahmen in der Produktion
    """
    # Sicherheitsheader hinzufügen
    def new_start_response(status, response_headers):
        # HTTPS erzwingen in Produktion
        if environ.get('HTTP_X_FORWARDED_PROTO') == 'http' and \
           os.environ.get('DJANGO_ENV') == 'production':
            status = '301 Moved Permanently'
            response_headers = [
                ('Location', f"https://{environ['HTTP_HOST']}{environ['PATH_INFO']}")
            ]
        
        # Sicherheitsheader hinzufügen
        security_headers = [
            ('X-Content-Type-Options', 'nosniff'),
            ('X-Frame-Options', 'DENY'),
            ('X-XSS-Protection', '1; mode=block'),
        ]
        response_headers.extend(security_headers)
        
        return start_response(status, response_headers)
    
    return application(environ, new_start_response)

# In Produktionsumgebungen die sichere Version verwenden
if os.environ.get('DJANGO_ENV') == 'production':
    application = application_with_security