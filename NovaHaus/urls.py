from django.contrib import admin
from django.urls import path, include
from main.views import (
    home, partner_view, services, portfolio, about, reviews, contact,
    calculator, calculate_cost, save_calculation, get_ai_recommendations,
    partner_success, blog, blog_post_detail, view_3d_model, privacy, chatbot
)
from django.conf import settings
from django.views.static import serve
from django.shortcuts import redirect



urlpatterns = [
    path('static/images/favicon/browserconfig.xml', serve, {
        'document_root': settings.STATIC_ROOT,
        'path': 'images/favicon/browserconfig.xml',
        'content_type': 'application/xml'
    }),
    path('admin/', admin.site.urls),  # Added admin URL
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('portfolio/', portfolio, name='portfolio'),
    path('about/', about, name='about'),
    path('reviews/', reviews, name='reviews'),
    path('contact/', contact, name='contact'),
    path('calculator/', calculator, name='calculator'),
    path('calculate_cost/', calculate_cost, name='calculate_cost'),
    path('save-calculation/', save_calculation, name='save_calculation'),
    path('get-ai-recommendations/', get_ai_recommendations, name='get_ai_recommendations'),
    path('partner-success/', partner_success, name='partner_success'),
    path('blog/', blog, name='blog'),
    path('blog/<int:post_id>/', blog_post_detail, name='blog_post_detail'),
    path('3d-viewer/', view_3d_model, name='view_3d_model'),
    path('privacy/', privacy, name='privacy'),
    path('chatbot/', chatbot, name='chatbot'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', serve, {'document_root': settings.STATIC_ROOT, 'path': 'robots.txt'}),
    path('partner/', partner_view, name='partner'),
    path('register-partner/', lambda request: redirect('partner'), name='register_partner'),
]

handler404 = 'main.views.page_not_found'
handler500 = 'main.views.custom_500'