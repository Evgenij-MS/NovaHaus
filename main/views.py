# main/views.py
from django.shortcuts import render

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