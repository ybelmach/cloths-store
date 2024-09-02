from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from uuid import uuid4

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from django.urls import reverse
import my_info


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


def two_fa(request):
    return render(request, 'users/two-fa.html')


def confirmation(request):
    if request.method == 'POST':
        if request.POST:
            email = request.POST['email']
            code = str(uuid4())
            code = code[:code.find('-')]
            send_mail(
                subject='Your code verification from online shop.',
                message=f"""Hello Blink Customer
    Please enter this verification code in site now to confirm your email address and complete the setup process:
    Your verification PIN:
    <h1>{code}</h1>
    This code expires 40 minutes from when it was sent. If the code is not entered, access to your account from the device will not be granted.
    If you'd like more information or assistance please view our FAQ or contact Customer Service.
    Thanks,
    The Blink Team""",
                from_email=my_info.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            print(f"[INFO] message to email was sent to {email}")


            return render(request, 'users/confirmation.html')
        else:
            return render(request, 'users/profile.html')
    else:
        print('1111111111111')
        return HttpResponseRedirect(reverse('users:profile'))









def forgot_password(request):
    return render(request, 'users/forgot_pass.html')


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
        'two_factor_required': True,
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
