from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from uuid import uuid4
from datetime import datetime
import pyotp

from carts.models import Cart
from orders.models import Order, OrderItem
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.urls import reverse
from users.utils import two_fa_sending
import my_info


def login(request):
    # Создание формы, авторизация
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)  # Проверка совпадений с БД

            session_key = request.session.session_key

            # if user.has_two_factor:
            #     user.is_verified = True
            #     user.save()
            #     return redirect(f'/user/confirmation/{user.username}')

            if user is not None:
                if user.has_two_factor:
                    two_fa_sending(request, user=user, path='users/confirmation.html')
                    request.session['username'] = user.username
                    return redirect('users:confirmation')
                auth.login(request, user)  # Логин пользователя
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
        'is_authenticated': request.user.is_authenticated,
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


def confirmation(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.session.get('username', None))[0]
        msg = f"{user.username}, Вы успешно вошли в аккаунт"
        if request.session.get('has_two_factor', False):
            msg = f"{user.username}, Вы успешно подключили двухфакторную аутентификацию!"
            user.has_two_factor = True
            user.save()
        otp_secret_key = request.session.get('otp_secret_key', None)
        otp_valid_time = request.session.get('otp_valid_time', None)
        otp = request.POST.get('code', None)
        if otp_valid_time and otp is not None:
            valid_until = datetime.fromisoformat(otp_valid_time)

            if valid_until > datetime.now():
                topt = pyotp.TOTP(otp_secret_key, interval=600)
                if topt.verify(otp):
                    auth.login(request, user)  # Логин пользователя
                    del request.session['otp_valid_time']
                    del request.session['otp_secret_key']
                    del request.session['username']
                    messages.success(request, msg)
                    return redirect('main:index')
    else:
        if request.user.is_authenticated:
            two_fa_sending(request, user=request.user, path='users/confirmation.html')
            request.session['username'] = request.user.username
            request.session['has_two_factor'] = True
        return render(request, 'users/confirmation.html')


def forgot_password(request):
    return render(request, 'users/forgot_pass.html')


@login_required
def profile(request):
    # Создание формы, регистрация
    if request.method == 'POST':
        code = request.POST.get('code', None)
        if code is not None:
            email = request.user.email
            user = User.objects.filter(email=email)[0]
            if user.verification_code == code:
                user.has_two_factor = True
                user.save()
                return render(request, 'users/profile.html')
        else:
            form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Данные успешно обновлены")

                # Перенаправление на страницу пользователя
                return HttpResponseRedirect(reverse('user:profile'))
    else:
        user = request.user

        form = ProfileForm(instance=request.user)

    orders = (
        Order.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")
    )

    context = {
        'title': 'Home - Кабинет',
        'form': form,
        'orders': orders,
        'two_factor_required': not User.objects.get(email=request.user.email).has_two_factor,
    }
    return render(request, 'users/profile.html', context)


def users_cart(request):
    return render(request, 'users/users-cart.html')


def logout(request):
    name = request.user.username

    if name:
        messages.success(request, f"{name}, Вы успешно вышли из аккаунта")
        auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def error(request):
    return render(request, 'users/error.html')
