from django.contrib import admin
from django.urls import path, re_path
from main import views

urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('get-ai-recommendations/', views.get_ai_recommendations, name='get_ai_recommendations'),
    path('save-calculation/', views.save_calculation, name='save_calculation'),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('calculator/', views.calculator, name='calculator'),
    re_path(r'^.*$', views.redirect_to_www), # Переместите редирект в конец
    path('register-partner/', views.register_partner, name='register_partner'),
    path('partner-success/', views.partner_success, name='partner_success'),
]