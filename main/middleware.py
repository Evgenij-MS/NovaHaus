class BlockBadBotsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        bad_bots = ['bot', 'crawler', 'spider', 'scanner']

        # Разрешаем Googlebot, проверяя его в user-agent
        if any(bot in user_agent for bot in bad_bots) and 'googlebot' not in user_agent:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Доступ запрещён')
        return self.get_response(request)