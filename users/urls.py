from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
    path('logout/', views.logout, name='logout'),
    path('forgot-pass/', views.forgot_password, name='forgot-pass'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('2fa-error/', views.error, name='fa_error'),
]
