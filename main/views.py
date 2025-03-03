# main/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from django.contrib.auth.forms import UserCreationForm


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

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')

        # Отправляем сообщение в OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Вы - помощник строительной компании NovaHaus. Отвечайте на вопросы клиентов."},
                {"role": "user", "content": user_message}
            ]
        )

        # Получаем ответ от AI
        bot_message = response['choices'][0]['message']['content']
        return JsonResponse({'response': bot_message})

    return JsonResponse({'error': 'Неподдерживаемый метод запроса'}, status=400)

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