from django.shortcuts import render

from goods.models import Categories


def index(request):
    categories = Categories.objects.all()

    contex = {
        'title': 'Home - Главная',
        'content': 'Магазин одежды HOME',
        'categories': categories,
    }
    return render(request, 'main/index.html', contex)


def about(request):
    context = {
        'title': 'Home - О нас',
        'name': 'Fashion House',
        'email': 'yaroslav.belmach.ln@gmail.com'
    }
    return render(request, 'main/about.html', context)


def delivery(request):
    context = {
        'title': 'Home - Доставка',
        'name': 'Fashion House',
        'email': 'yaroslav.belmach.ln@gmail.com',
        'adress': 'улица Семашко, 35А, Минск',
    }
    return render(request, 'main/delivery.html', context)
