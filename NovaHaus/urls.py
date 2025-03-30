from django.contrib import admin
from django.urls import path, include, re_path
from main import views
from main.views import view_3d_model
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.defaults import page_not_found


def block_sensitive_paths(request, *args, **kwargs):
    """Блокировка доступа к чувствительным путям"""
    return HttpResponseForbidden(
        "<h1>Доступ запрещен</h1><p>Запрос к защищенному ресурсу</p>",
        content_type="text/html"
    )

# Базовые URL-адреса
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Добавление защищенных маршрутов
for sensitive_path in [
    r'^\.env', r'^wp-', r'^config', r'^\.git',
    r'^phpmyadmin', r'^backup', r'\.sql$',
    r'\.bak$', r'\.log$'
]:
    urlpatterns += [
        re_path(sensitive_path, block_sensitive_paths)
    ]

# URL-адреса с поддержкой языков
urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('calculator/', views.calculator, name='calculator'),
    path('register-partner/', views.register_partner, name='register_partner'),
    path('partner-success/', views.partner_success, name='partner_success'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('get-ai-recommendations/', views.get_ai_recommendations, name='get_ai_recommendations'),
    path('save-calculation/', views.save_calculation, name='save_calculation'),
    path('3d-viewer/', view_3d_model, name='3d_viewer'),
    prefix_default_language=False
)

# Отладка - только для разработки
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)