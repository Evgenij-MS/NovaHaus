

class BlockBadBotsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        bad_bots = ['bot', 'crawler', 'spider', 'scanner']

        if any(bot in user_agent for bot in bad_bots):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Access denied')

        return self.get_response(request)