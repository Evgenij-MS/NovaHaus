from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Calculation, Partner, BlogPost
from .forms import PartnerForm
import json
import requests
import logging
import os
import uuid
from django.utils.translation import activate
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page



# Настройка
logger = logging.getLogger(__name__)


# API-ключ DeepSeek
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Функция смены языка
def set_language(request, language):
    if language in [lang[0] for lang in settings.LANGUAGES]:
        activate(language)
        request.session[settings.LANGUAGE_COOKIE_NAME] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Перенаправление на главную, если HTTP_REFERER отсутствует



# # Редирект на www
def redirect_to_www(request):
    # Проверяем, что запрос уже не идет на www
    if not request.get_host().startswith('www.'):
        return HttpResponsePermanentRedirect(f"https://www.novahaus-koeln.de{request.path or '/'}")
    return None  # Если уже на www, не выполняем редирект



# Чат-бот
@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        language = request.POST.get('language', 'ru')

        if language not in [lang[0] for lang in settings.LANGUAGES]:
            language = 'ru'  # Используем язык по умолчанию

        system_message = {
            'ru': "Вы - помощник строительной компании NovaHaus. Отвечайте на вопросы клиентов.",
            'en': "You are an assistant for the construction company NovaHaus. Answer customer questions.",
            'de': "Sie sind ein Assistent für das Bauunternehmen NovaHaus. Beantworten Sie Kundenfragen."
        }

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_message[language]},
                {"role": "user", "content": user_message}
            ]
        }

        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            bot_message = response.json()['choices'][0]['message']['content']
            return JsonResponse({'response': bot_message})
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к DeepSeek: {e}")
            return JsonResponse({'error': 'Ошибка при обработке запроса'}, status=500)
        except KeyError as e:
            logger.error(f"Ошибка в структуре ответа DeepSeek: {e}")
            return JsonResponse({'error': 'Ошибка при обработке ответа'}, status=500)

    return JsonResponse({'error': 'Неподдерживаемый метод запроса'}, status=400)


# Получение рекомендаций от AI
@csrf_exempt
def get_ai_recommendations(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total_cost = data.get('totalCost', 0)
            material_cost = data.get('materialCost', 0)
            labor_cost = data.get('laborCost', 0)
            work_type = data.get('workType', '')
            area = data.get('area', 0)

            if not all([total_cost, material_cost, labor_cost, work_type, area]):
                return JsonResponse({'success': False, 'error': 'Недостаточно данных'}, status=400)

            recommendation = f"Для типа работы '{work_type}' с площадью {area} м² рекомендуется вложить {total_cost} в проект, где стоимость материалов составляет {material_cost}, а стоимость труда — {labor_cost}."

            return JsonResponse({'success': True, 'recommendation': recommendation}, status=200)
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON: {e}")
            return JsonResponse({'success': False, 'error': 'Некорректный формат данных'}, status=400)
        except Exception as e:
            logger.error(f"Ошибка сервера: {e}")
            return JsonResponse({'success': False, 'error': 'Ошибка сервера'}, status=500)

    return JsonResponse({'success': False, 'error': 'Метод запроса должен быть POST'}, status=400)




# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


# Регистрация партнера
def register_partner(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save(commit=False)
            partner.referral_code = str(uuid.uuid4())[:8]
            while Partner.objects.filter(referral_code=partner.referral_code).exists():
                partner.referral_code = str(uuid.uuid4())[:8]
            partner.save()
            return redirect('partner_success')
    else:
        form = PartnerForm()
    return render(request, 'main/register_partner.html', {'form': form})



# Сохранение расчёта
@csrf_exempt
def save_calculation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if not all(key in data for key in ['workType', 'area', 'material', 'includeMaterials', 'urgency', 'totalCost', 'materialCost', 'laborCost']):
                return JsonResponse({'success': False, 'error': 'Неверные данные'}, status=400)

            Calculation.objects.create(
                user=request.user,
                work_type=data['workType'],
                area=data['area'],
                material=data['material'],
                include_materials=data['includeMaterials'],
                urgency=data['urgency'],
                total_cost=data['totalCost'],
                material_cost=data['materialCost'],
                labor_cost=data['laborCost']
            )
            return JsonResponse({'success': True})
        except KeyError as e:
            logger.error(f"Ошибка в данных: {e}")
            return JsonResponse({'success': False, 'error': 'Неверные данные'}, status=400)
        except Exception as e:
            logger.error(f"Ошибка при сохранении расчёта: {e}")
            return JsonResponse({'success': False, 'error': 'Ошибка сервера'}, status=500)
    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод запроса'}, status=400)


@cache_page(60 * 15)  # Кеширование на 15 минут


# Основные страницы
def home(request):
    return render(request, 'main/home.html')

def services(request):
    return render(request, 'main/services.html')

def portfolio(request):
    return render(request, 'main/portfolio.html')

def about(request):
    return render(request, 'main/about.html')

def reviews(request):
    return render(request, 'main/reviews.html')

def blog(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'main/blog.html', {'blog_posts': blog_posts})

def contact(request):
    return render(request, 'main/contact.html')

def calculator(request):
    return render(request, 'main/calculator.html')

# Страница успешной регистрации партнёра
def partner_success(request):
    return render(request, 'main/partner_success.html')

# Детальная страница блога
def blog_post_detail(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'main/blog_post_detail.html', {'post': post})


# Просмотр 3D модели
def view_3d_model(request):
    return render(request, 'main/3d_viewer.html')
