from django.contrib import admin
from django.urls import path, re_path
from main import views  # Импорт всего файла views
from main.views import view_3d_model  # Импорт конкретной функции

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Основные страницы
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('calculator/', views.calculator, name='calculator'),

    # Регистрация
    path('register-partner/', views.register_partner, name='register_partner'),
    path('partner-success/', views.partner_success, name='partner_success'),

    # Чат-бот и AI
    path('chatbot/', views.chatbot, name='chatbot'),
    path('get-ai-recommendations/', views.get_ai_recommendations, name='get_ai_recommendations'),

    # Расчёты
    path('save-calculation/', views.save_calculation, name='save_calculation'),

    # Просмотр 3D-модели
    path('3d-viewer/', view_3d_model, name='3d_viewer'),

    # Редирект на www (должен быть в конце)
    re_path(r'^.*$', views.redirect_to_www),
]
