from django.urls import path, include
from main import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('contact/', views.contact, name='contact'),
    path('calculator/', views.calculator, name='calculator'),
    path('calculate_cost/', views.calculate_cost, name='calculate_cost'),
    path('save-calculation/', views.save_calculation, name='save_calculation'),
    path('get-ai-recommendations/', views.get_ai_recommendations, name='get_ai_recommendations'),
    path('partner-success/', views.partner_success, name='partner_success'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_post_detail, name='blog_post_detail'),
    path('3d-viewer/', views.view_3d_model, name='view_3d_model'),
    path('privacy/', views.privacy, name='privacy'),
    path('register-partner/', views.register_partner, name='register_partner'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('i18n/', include('django.conf.urls.i18n')),
    # Добавляем маршрут для robots.txt
    path('robots.txt', serve, {'document_root': settings.STATIC_ROOT, 'path': 'robots.txt'}),
]


handler404 = 'main.views.page_not_found'
handler500 = 'main.views.custom_500'