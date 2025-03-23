from django.contrib import admin
from django.urls import path, re_path, include
from main import views  # Импорт всего файла views
from main.views import view_3d_model, redirect_to_www  # Импорт конкретной функции
from django.conf.urls.i18n import i18n_patterns
# from django.views.generic.base import RedirectView

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Поддержка переключения языка
    path('i18n/', include('django.conf.urls.i18n')),
]

# Локализованные URL
urlpatterns += i18n_patterns(
    # Основные страницы
    path('', views.home, name='home'),  # Главная страница
    path('services/', views.services, name='services'),  # Страница услуг
    path('portfolio/', views.portfolio, name='portfolio'),  # Портфолио
    path('about/', views.about, name='about'),  # О компании
    path('reviews/', views.reviews, name='reviews'),  # Отзывы клиентов
    path('blog/', views.blog, name='blog'),  # Блог
    path('contact/', views.contact, name='contact'),  # Контакты
    path('calculator/', views.calculator, name='calculator'),  # Калькулятор

    # Регистрация
    path('register-partner/', views.register_partner, name='register_partner'),  # Регистрация партнера
    path('partner-success/', views.partner_success, name='partner_success'),  # Успешная регистрация партнера

    # Чат-бот и AI
    path('chatbot/', views.chatbot, name='chatbot'),  # Чат-бот
    path('get-ai-recommendations/', views.get_ai_recommendations, name='get_ai_recommendations'),  # Рекомендации AI

    # Расчёты
    path('save-calculation/', views.save_calculation, name='save_calculation'),  # Сохранение расчёта

    # Просмотр 3D-модели
    path('3d-viewer/', view_3d_model, name='3d_viewer'),  # Просмотр 3D-модели
)

# Редирект на www (должен быть в конце)
urlpatterns += [
    re_path(r'^.*$', redirect_to_www),
]

