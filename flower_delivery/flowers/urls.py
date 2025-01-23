from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'flowers'  # Это пространство имен

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),  # О нас
    path('contacts/', views.contacts, name='contacts'),  # Контакты
]
