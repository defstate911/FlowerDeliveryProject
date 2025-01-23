from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Добавляем для сообщений об ошибке
# Вход пользователя
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')  # Перенаправление на главную
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Регистрация пользователя
def signup_view(request):
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Создаем нового пользователя
            return redirect('registration:login')  # Перенаправление на страницу входа
        #else:
            # Добавляем отладочные сообщения, чтобы узнать, что пошло не так
            #messages.error(request, form.errors.as_json())
            #print("Ошибки формы:", form.errors)  # Вывод ошибок в консоль
    else:
        form = CustomUserCreationForm()
        #form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Личный кабинет (доступен только для вошедших пользователей)
# @login_required
# def profile_view(request):
#     return render(request, 'registration/profile.html', {'user': request.user})

# Выход пользователя
def logout_view(request):
    logout(request)
    #return redirect('registration/login')  # Перенаправление на страницу входа
    #form = AuthenticationForm()
    #return render(request, 'registration/login.html', {'form': form})
    #return render(request, 'flowers/index.html')
    return redirect('flowers:home')