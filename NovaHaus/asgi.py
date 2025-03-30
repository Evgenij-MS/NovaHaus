import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from main.routing import websocket_urlpatterns  # Импорт WebSocket маршрутов

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NovaHaus.settings')

# Инициализация Django ASGI приложения заранее для работы с Workers
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})