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

# Конфигурация API
GROK_API_KEY = os.getenv('GROK_API_KEY')
GROK_API_URL = "https://api.x.ai/v1/chat/completions"  # Официальный endpoint Grok 3


def page_not_found(request, _exception):
    return render(request, 'main/404.html', status=404)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def save_uploaded_file(file, subfolder):
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


@csrf_exempt
def set_language(request, lang_code):
    """Установка языка с редирект."""
    if request.method == 'POST':
        lang_code = request.POST.get('language', lang_code)
        if lang_code in dict(settings.LANGUAGES):
            translation.activate(lang_code)
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code, max_age=365 * 24 * 60 * 60)

            # Обновление URL с учётом языкового префикса
            current_path = request.path
            new_path = current_path.replace(
                r'^/(de|en|tr|ru)/', f'/{lang_code}/'
            )
            if new_path == current_path:
                new_path = f'/{lang_code}{current_path}'
            return HttpResponseRedirect(new_path)

    return JsonResponse({'success': False, 'error': 'Invalid language or method'}, status=400)


@csrf_exempt
def chatbot(request):
    """Чат-бот с Grok 3."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешён'}, status=405)

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
            # noqa: E501
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
def save_calculation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            calculation = Calculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                data=data
            )
            return JsonResponse({'success': True, 'id': calculation.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Требуется POST-запрос'}, status=405)


def home(request):
    # Запрашиваем до 8 услуг, 4 проекта и 5 отзывов для главной страницы
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
    return render(request, 'main/services.html')


def portfolio(request):
    return render(request, 'main/portfolio.html')


def about(request):
    return render(request, 'main/about.html')


def reviews(request):
    return render(request, 'main/reviews.html')


def contact(request):
    return render(request, 'main/contact.html')


def calculator(request):
    return render(request, 'main/calculator.html')


def partner_success(request):
    return render(request, 'main/partner_success.html')


def blog(request):
    posts = BlogPost.objects.all().order_by('-published_date')
    return render(request, 'main/blog.html', {
        'blog_posts': posts,
        'meta_description': 'Статьи о ремонте и строительстве от NovaHaus'
    })


def blog_post_detail(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    return render(request, 'main/blog_post_detail.html', {'post': post})


def view_3d_model(request):
    return render(request, 'main/3d_viewer.html')


@csrf_exempt
def get_ai_recommendations(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Требуется POST-запрос'}, status=405)

    try:
        data = json.loads(request.body)
        required_fields = ['totalCost', 'materialCost', 'laborCost', 'workType', 'area']

        if not all(field in data for field in required_fields):
            return JsonResponse({'success': False, 'error': 'Неполные данные'}, status=400)

        system_prompt = {
            'de': "Sie sind Grok 3, Assistent von NovaHaus. Geben Sie Empfehlungen für ein Bauprojekt.",
            'en': "You are Grok 3, assistant for NovaHaus. Provide recommendations for a construction project.",
            'tr': "Siz Grok 3, NovaHaus asistanısınız. Bir inşaat projesi için öneriler sunun.",  # noqa: E501
            'ru': "Вы Grok 3, ассистент NovaHaus. Дайте рекомендации для строительного проекта."
        }.get(data.get('language', 'de'), 'de')

        prompt = (
            f"Я строительная компания NovaHaus. Дайте рекомендации для проекта:\n"
            f"- Тип работы: {data['workType']}\n"
            f"- Площадь: {data['area']} м²\n"
            f"- Общий бюджет: €{data['totalCost']}\n"
            f"- Стоимость материалов: €{data['materialCost']}\n"
            f"- Стоимость работы: €{data['laborCost']}\n"
            f"Ответьте профессионально на {data.get('language', 'de')}."
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
        return JsonResponse({'success': True, 'recommendation': recommendation})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Неверный JSON'}, status=400)
    except requests.exceptions.RequestException:
        return JsonResponse({'success': False, 'error': 'Ошибка подключения к Grok'}, status=502)
    except Exception as e:
        logger.error(f"Ошибка рекомендаций: {str(e)}")
        return JsonResponse({'success': False, 'error': 'Ошибка обработки'}, status=500)


def register_partner(request):
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
    code = uuid.uuid4().hex[:8].upper()
    while Partner.objects.filter(referral_code=code).exists():
        code = uuid.uuid4().hex[:8].upper()
    return code