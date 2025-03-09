from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Calculation
import json
from django.core.files.storage import default_storage
import requests
import logging


logger = logging.getLogger(__name__)

# API-ключ DeepSeek
DEEPSEEK_API_KEY = "sk-0efe6828d940403ba98475c70df6f384"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Убедитесь, что URL правильный


# Чат-бот
@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        language = request.POST.get('language', 'ru')

        # Настройка языка для AI
        system_message = {
            'ru': "Вы - помощник строительной компании NovaHaus. Отвечайте на вопросы клиентов.",
            'en': "You are an assistant for the construction company NovaHaus. Answer customer questions.",
            'de': "Sie sind ein Assistent für das Bauunternehmen NovaHaus. Beantworten Sie Kundenfragen."
        }

        # Формируем запрос к DeepSeek
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
            bot_message = response.json()['choices'][0]['message']['content']
            return JsonResponse({'response': bot_message})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Неподдерживаемый метод запроса'}, status=400)

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

# Сохранение расчета
@csrf_exempt
def save_calculation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        calculation = Calculation.objects.create(
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
    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод запроса'}, status=400)

# Загрузка документов
@csrf_exempt
def upload_document(request):
    if request.method == 'POST' and request.FILES['document']:
        document = request.FILES['document']
        file_name = default_storage.save(document.name, document)
        # Сохраняем информацию о файле в базе данных (пример)
        # Document.objects.create(user=request.user, file=file_name)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод запроса'}, status=400)

# Отправка сообщения менеджеру
@csrf_exempt
def send_message_to_manager(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data['message']
        # Сохраняем сообщение в базе данных (пример)
        # Message.objects.create(user=request.user, message=message, is_manager=False)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод запроса'}, status=400)

# AI-рекомендации для калькулятора
@csrf_exempt
def get_ai_recommendations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        work_type = data.get('workType')
        area = data.get('area')
        total_cost = data.get('totalCost')
        material_cost = data.get('materialCost')
        labor_cost = data.get('laborCost')

        prompt = f"""
        Вы - помощник строительной компании NovaHaus. Клиент рассчитал стоимость работ:
        - Тип работ: {work_type}
        - Площадь: {area} м²
        - Общая стоимость: {total_cost} €
        - Стоимость материалов: {material_cost} €
        - Стоимость работы: {labor_cost} €

        Дайте рекомендации по оптимизации затрат или улучшению качества работ.
        """

        # Формируем запрос к DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            recommendation = response.json()['choices'][0]['message']['content']
            return JsonResponse({'success': True, 'recommendation': recommendation})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод запроса'}, status=400)



@csrf_exempt
def get_ai_recommendations(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")
            # ... ваш код ...
        except Exception as e:
            logger.error(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})



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
    return render(request, 'main/blog.html')

def contact(request):
    return render(request, 'main/contact.html')

def calculator(request):
    return render(request, 'main/calculator.html')