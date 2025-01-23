from django.urls import path
from . import views  # или другой путь для ваших представлений
from django.contrib.auth import views as auth_views

app_name = 'registration'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  # Регистрация пользователя
    path('login/', views.login_view, name='login'),  # Вход пользователя
    path('logout/', views.logout_view, name='logout'),  # Выход
    #path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Выход
    #path('logout/', auth_views.LogoutView.as_view(next_page='flowers:home'), name='logout'),  # Выход
]




