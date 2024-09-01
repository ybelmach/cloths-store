from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.urls import reverse


def login(request):
    # Создание формы, авторизация
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы успешно вошли в аккаунт")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.GET.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))

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

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"{user.username}, Вы успешно зарегестрировались и вошли в аккаунт")

            # Перенаправление на страницу входа
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    contex = {
        'title': 'Home - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', contex)


@login_required
def profile(request):
    # Создание формы, регистрация
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные успешно обновлены")

            # Перенаправление на страницу пользователя
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    orders = (
        Order.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")
    )

    contex = {
        'title': 'Home - Кабинет',
        'form': form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', contex)


def users_cart(request):
    return render(request, 'users/users-cart.html')


def logout(request):
    name = request.user.username

    if name:
        messages.success(request, f"{name}, Вы успешно вышли из аккаунта")
        auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))
