from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect

from users.forms import UserLoginForm, UserRegistrationForm
from django.urls import reverse

def login(request):

    # Создание формы, авторизация
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                # Перенаправление на главную страницу
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    contex = {
        'title': 'Home - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', contex)


def registration(request):
    # Создание формы, регистрация
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            # Перенаправление на страницу входа
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    contex = {
        'title': 'Home - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', contex)


def profile(request):
    contex = {
        'title': 'Home - Кабинет',
    }
    return render(request, 'users/profile.html', contex)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))
