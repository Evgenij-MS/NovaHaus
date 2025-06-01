import os
import json
import logging
import uuid
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import translation
from .forms import PartnerForm
from .models import Service, Portfolio, Review, Calculation, Partner, BlogPost, ChatLog

logger = logging.getLogger(__name__)

GROK_API_KEY = os.getenv('GROK_API_KEY')
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

def partner_view(request):
    return render(request, 'main/partner.html')

def page_not_found(request, _exception):
    """Обработка ошибки 404."""
    return render(request, 'main/404.html', status=404)

def get_client_ip(request):
    """Получение IP-адреса клиента."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

def save_uploaded_file(file, subfolder):
    """Сохранение загруженного файла."""
    fs = FileSystemStorage(location=subfolder)
    filename = f"{uuid.uuid4().hex[:8]}_{file.name}"
    saved_name = fs.save(filename, file)
    return fs.url(saved_name)

def _make_grok_api_request(payload, timeout=10):
    """Отправка запроса к API Grok."""
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API Grok: {str(e)}")
        raise

def get_current_construction_index():
    """Получение текущего индекса строительных затрат из Eurostat."""
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_copi_q?format=JSON&lang=EN&geo=DE&indic_bt=CC&unit=I15&s_adj=NSA&nace_r2=F"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        time_periods = data['dimension']['time']['category']['index']
        latest_time = max(time_periods, key=lambda x: time_periods[x])
        value = data['value'][str(time_periods[latest_time])]
        return float(value)
    except Exception as e:
        logger.error(f"Ошибка получения индекса Eurostat: {str(e)}")
        return 100.0

@csrf_exempt
def set_language(request, lang_code):
    """Установка языка с редиректом."""
    if request.method == 'POST':
        lang_code = request.POST.get('language', lang_code)
        if lang_code in dict(settings.LANGUAGES):
            translation.activate(lang_code)
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code, max_age=365 * 24 * 60 * 60)
            current_path = request.path
            new_path = current_path.replace(r'^/(de|en|tr|ru)/', f'/{lang_code}/')
            if new_path == current_path:
                new_path = f'/{lang_code}{current_path}'
            return HttpResponseRedirect(new_path)
    return JsonResponse({'success': False, 'error': 'Недопустимый язык или метод'}, status=400)

@csrf_exempt
def chatbot(request):
    """Чат-бот с Grok 3."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        language = data.get('language', 'de')
        if language not in dict(settings.LANGUAGES):
            language = 'de'
        ChatLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            message=user_message[:500],
            language=language,
            ip_address=get_client_ip(request)
        )
        system_prompt = {
            'de': "Sie sind Grok 3, entwickelt von xAI, Assistent für das Bauunternehmen NovaHaus. Antworten Sie professionell auf Deutsch.",
            'en': "You are Grok 3, created by xAI, assistant for NovaHaus construction company. Respond professionally in English.",
            'tr': "Siz Grok 3, xAI tarafından geliştirilmiş, NovaHaus inşaat şirketi asistanısınız. Profesyonelce Türkçe yanıt verin.",
            'ru': "Вы Grok 3, созданный xAI, ассистент строительной компании NovaHaus. Отвечайте профессионально на русском."
        }.get(language, 'de')
        payload = {
            "model": "grok-3",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        bot_response = _make_grok_api_request(payload)
        return JsonResponse({'response': bot_response})
    except requests.exceptions.RequestException:
        return JsonResponse({'error': 'Ошибка подключения к сервису Grok'}, status=502)
    except Exception as e:
        logger.error(f"Ошибка чат-бота: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)

@csrf_exempt
def calculate_cost(request):
    """Рассчитать трудовые затраты на основе типа работ и площади."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Требуется POST-запрос'}, status=405)
    try:
        work_type = request.POST.get('work-type')
        area = float(request.POST.get('area'))

        if area <= 0:
            return JsonResponse({'success': False, 'error': 'Площадь должна быть больше 0'}, status=400)

        service = Service.objects.filter(category=work_type).first()
        if not service or not service.labor_cost_per_m2:
            return JsonResponse({'success': False, 'error': 'Услуга не найдена или трудовые затраты не указаны'}, status=400)

        labor_cost = float(service.labor_cost_per_m2) * area

        return JsonResponse({
            'success': True,
            'labor_cost': labor_cost,
            'work_type': work_type,
            'area': area
        })
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Неверный формат данных'}, status=400)
    except Exception as e:
        logger.error(f"Ошибка расчета: {str(e)}")
        return JsonResponse({'success': False, 'error': 'Ошибка обработки'}, status=500)

@csrf_exempt
def save_calculation(request):
    """Сохранение расчета."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            calculation = Calculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                work_type=data.get('workType', ''),
                area=data.get('area', 0),
                material=data.get('material', ''),
                total_cost=data.get('totalCost', 0),
                material_cost=data.get('materialCost', 0),
                labor_cost=data.get('laborCost', 0),
                data=data
            )
            return JsonResponse({'success': True, 'id': calculation.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Требуется POST-запрос'}, status=405)

def home(request):
    """Главная страница."""
    service_list = Service.objects.all()[:8]
    project_list = Portfolio.objects.all()[:4]
    review_list = Review.objects.all()[:5]
    context = {
        'services': service_list,
        'projects': project_list,
        'reviews': review_list,
    }
    return render(request, 'main/home.html', context)

def services(request):
    """Страница услуг."""
    service_list = Service.objects.all()
    return render(request, 'main/services.html', {'services': service_list})

def portfolio(request):
    """Страница портфолио."""
    project_list = Portfolio.objects.all()
    return render(request, 'main/portfolio.html', {'projects': project_list})

def about(request):
    """Страница о компании."""
    return render(request, 'main/about.html')

def reviews(request):
    """Страница отзывов."""
    review_list = Review.objects.all()
    return render(request, 'main/reviews.html', {'reviews': review_list})

def contact(request):
    """Страница контактов."""
    return render(request, 'main/contact.html')

def calculator(request):
    """Страница калькулятора."""
    return render(request, 'main/calculator.html')

def partner_success(request):
    """Страница успешной регистрации партнера."""
    return render(request, 'main/partner_success.html')

def blog(request):
    """Страница блога."""
    posts = BlogPost.objects.all().order_by('-published_date')
    return render(request, 'main/blog.html', {
        'blog_posts': posts,
        'meta_description': 'Статьи о ремонте и строительстве от NovaHaus'
    })

def blog_post_detail(request, post_id):
    """Страница статьи блога."""
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'main/blog_post_detail.html', {'post': post})

def view_3d_model(request):
    """Страница 3D-просмотра."""
    return render(request, 'main/3d_viewer.html')

def privacy(request):
    """Страница политики конфиденциальности."""
    return render(request, 'main/privacy.html')

@csrf_exempt
def get_ai_recommendations(request):
    """Получение AI-рекомендаций по материалам."""
    if request.method == 'GET':
        return JsonResponse({'error': 'Используйте POST для рекомендаций'}, status=405)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['laborCost', 'workType', 'area', 'materialQuality']
            if not all(field in data for field in required_fields):
                return JsonResponse({'success': False, 'error': 'Неполные данные'}, status=400)

            service = Service.objects.filter(category=data['workType']).first()
            if not service or not service.base_material_cost_per_m2:
                return JsonResponse({'success': False, 'error': 'Услуга не найдена или стоимость материалов не указана'}, status=400)

            material_modifiers = {
                'economy': 0.8,
                'standard': 1.0,
                'premium': 1.5
            }
            modifier = material_modifiers.get(data['materialQuality'], 1.0)
            material_cost = float(service.base_material_cost_per_m2) * modifier * float(data['area'])

            system_prompt = {
                'de': "Sie sind Grok 3, Assistent von NovaHaus. Geben Sie Empfehlungen für ein Bauprojekt.",
                'en': "You are Grok 3, assistant for NovaHaus. Provide recommendations for a construction project.",
                'tr': "Siz Grok 3, NovaHaus asistanısınız. Bir inşaat projesi için öneriler sunun.",
                'ru': "Вы Grok 3, ассистент NovaHaus. Дайте рекомендации для строительного проекта."
            }.get(data.get('language', 'de'), 'de')
            prompt = (
                f"Я строительная компания NovaHaus. Для проекта типа {data['workType']} с площадью {data['area']} м² "
                f"и выбранным качеством материалов {data['materialQuality']}, трудовые затраты составляют €{data['laborCost']}. "
                f"Примерная стоимость материалов: €{material_cost}. Дайте рекомендации по материалам и их использованию."
            )
            payload = {
                "model": "grok-3",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            recommendation = _make_grok_api_request(payload)
            return JsonResponse({
                'success': True,
                'recommendation': recommendation,
                'material_cost': material_cost
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Неверный JSON'}, status=400)
        except requests.exceptions.RequestException:
            return JsonResponse({'success': False, 'error': 'Ошибка подключения к Grok'}, status=502)
        except Exception as e:
            logger.error(f"Ошибка рекомендаций: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Ошибка обработки'}, status=500)

def register_partner(request):
    """Регистрация партнера."""
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save(commit=False)
            partner.referral_code = generate_unique_referral()
            partner.save()
            return redirect('partner_success')
    else:
        form = PartnerForm()
    return render(request, 'main/register_partner.html', {
        'form': form,
        'meta_title': 'Регистрация партнера'
    })

def generate_unique_referral():
    """Генерация уникального реферального кода."""
    code = uuid.uuid4().hex[:8].upper()
    while Partner.objects.filter(referral_code=code).exists():
        code = uuid.uuid4().hex[:8].upper()
    return code

def custom_500(request):
    """Обработка ошибки 500."""
    return render(request, 'main/500.html', status=500)