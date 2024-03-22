from django.shortcuts import render


def index(request):
    contex = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME',
    }
    return render(request, 'main/index.html', contex)


def about(request):
    context = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст',
    }
    return render(request, 'main/about.html', context)
