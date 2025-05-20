import re
from django.http import HttpResponseForbidden
from django.conf import settings

class BlockBadBotsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Разрешаем доступ к определённым путям для всех агентов
        allowed_paths = ['/favicon.ico', '/robots.txt', '/sitemap.xml']
        if request.path in allowed_paths:
            return self.get_response(request)

        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        # Разрешаем известных поисковых ботов
        if any(pattern.search(user_agent) for pattern in settings.ALLOWED_CRAWLERS):
            return self.get_response(request)

        # Блокируем запрещённых агентов
        if any(pattern.search(user_agent) for pattern in settings.DISALLOWED_USER_AGENTS):
            return HttpResponseForbidden('Доступ запрещён')

        return self.get_response(request)