from django.shortcuts import render


def login(request):
    contex = {
        'title': 'Home - Авторизация'
    }
    return render(request, 'users/login.html', contex)


def registration(request):
    contex = {
        'title': 'Home - Решистрация'
    }
    return render(request, 'users/registration.html', contex)


def profile(request):
    contex = {
        'title': 'Home - Кабинет'
    }
    return render(request, 'users/profile.html', contex)


def logout(request):
    ...
