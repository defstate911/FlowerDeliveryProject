from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Имя пользователя"
        self.fields['email'].label = "Электронная почта"
        self.fields['phone'].label = "Телефон"
        self.fields['address'].label = "Адрес"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтверждение пароля"

    def save(self, commit=True):
        user = super().save(commit=False)  # Сначала создаем пользователя
        user.phone = self.cleaned_data['phone']  # Присваиваем телефон
        user.address = self.cleaned_data['address']  # Присваиваем адрес
        if commit:
            user.save()  # Сохраняем пользователя в базе данных
        return user

    def save1(self, commit=True):
        return super().save(commit=commit)


