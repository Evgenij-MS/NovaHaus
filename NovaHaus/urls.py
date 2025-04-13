from django.contrib import admin
from django.urls import path, include, re_path
from main import views
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.http import HttpResponseForbidden

def block_sensitivity_paths(request):
    """Блокирует доступ к чувствительным путям (.env, .git и т.д.)"""
    return HttpResponseForbidden(
        "<h1>Доступ запрещён</h1><p>Запрос к защищённому ресурсу</p>",
        content_type="text/html"
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

sensitive_paths = [
    r'^\.env', r'^wp-', r'^config', r'^\.git',
    r'^phpmyadmin', r'^backup', r'\.sql$',
    r'\.bak$', r'\.log$'
]

for sensitive_path in sensitive_paths:
    urlpatterns += [re_path(sensitive_path, block_sensitivity_paths)]

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
    path('3d-viewer/', views.view_3d_model, name='3d_viewer'),
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
    prefix_default_language=True
)

if settings.DEBUG:
    from django.conf.urls.static import static
    # Обслуживание статических и медиафайлов в режиме отладки
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Кастомная страница 404
handler404 = 'main.views.page_not_found'