from django.shortcuts import render
from .models import Bouquet

def home(request):
    bouquets = Bouquet.objects.all()  # Получаем все букеты из базы данных
    return render(request, 'flowers/index.html', {"bouquets": bouquets})

def about(request):
    return render(request, 'flowers/about.html')

def contacts(request):
    return render(request, 'flowers/contacts.html')
