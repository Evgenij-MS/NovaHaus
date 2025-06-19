
import os
import logging
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Logging konfigurieren
logger = logging.getLogger(__name__)

# Django Settings Module setzen
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NovaHaus.settings')

# Django ASGI-Anwendung zuerst initialisieren
django_asgi_app = get_asgi_application()

# WebSocket-URL-Patterns definieren (falls routing.py nicht existiert)
websocket_urlpatterns = []

# Versuche WebSocket-Routen zu importieren
try:
    from main.routing import websocket_urlpatterns as imported_patterns
    websocket_urlpatterns = imported_patterns
    logger.info("WebSocket-Routen erfolgreich importiert")
except ImportError as e:
    logger.warning(f"Konnte WebSocket-Routen nicht importieren: {e}")
    logger.info("Verwende leere WebSocket-Konfiguration")

# ASGI-Anwendung konfigurieren
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})