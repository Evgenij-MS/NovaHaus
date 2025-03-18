from django.urls import path
from .consumers import AIConsumer  # Импорт вашего WebSocket-консьюмера

websocket_urlpatterns = [
    path('ws/ai/', AIConsumer.as_asgi()),  # Маршрут для WebSocket соединений
]
