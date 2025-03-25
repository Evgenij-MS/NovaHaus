from django.contrib import admin
from django.urls import path, include
from main import views  # Импорт всего файла views
from main.views import view_3d_model, home  # Импорт конкретной функции
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),    # Админка
    path('i18n/', include('django.conf.urls.i18n')),  # Поддержка переключения языка
]


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
)