from django.shortcuts import render

from goods.models import Categories


def index(request):

    categories = Categories.objects.all()

    contex = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME',
        'categories': categories,
    }
    return render(request, 'main/index.html', contex)


def about(request):
    context = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст',
    }
    return render(request, 'main/about.html', context)
