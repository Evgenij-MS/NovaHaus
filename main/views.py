# main/views.py
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import openai
from django.contrib.auth.forms import UserCreationForm
from .models import Calculation
import json
from django.core.files.storage import default_storage


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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message[language]},
                {"role": "user", "content": user_message}
            ]
        )

        bot_message = response['choices'][0]['message']['content']
        return JsonResponse({'response': bot_message})

    return JsonResponse({'error': 'Неподдерживаемый метод запроса'}, status=400)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

openai.api_key = "ВАШ_API_КЛЮЧ_OPENAI"




def save_calculation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Сохраняем расчет в базе данных (пример)
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

def upload_document(request):
    if request.method == 'POST' and request.FILES['document']:
        document = request.FILES['document']
        file_name = default_storage.save(document.name, document)
        # Сохраняем информацию о файле в базе данных (пример)
        # Document.objects.create(user=request.user, file=file_name)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод запроса'}, status=400)


def send_message_to_manager(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data['message']
        # Сохраняем сообщение в базе данных (пример)
        # Message.objects.create(user=request.user, message=message, is_manager=False)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Неподдерживаемый метод запроса'}, status=400)


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