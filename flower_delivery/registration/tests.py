from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegistrationTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com",
            "phone": "1234567890",
            "address": "123 Test St.",
        }
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"],
            phone=self.user_data["phone"],
            address=self.user_data["address"],
        )

    def test_signup_view_get(self):
        """Проверяет, что страница регистрации открывается корректно"""
        response = self.client.get(reverse("registration:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_view_post(self):
        """Проверяет успешную регистрацию нового пользователя"""
        signup_data = {
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "email": "newuser@example.com",
            "phone": "9876543210",
            "address": "456 Another St.",
        }
        response = self.client.post(reverse("registration:signup"), data=signup_data)
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу входа
        self.assertTrue(self.user_model.objects.filter(username="newuser").exists())

    def test_login_view_get(self):
        """Проверяет, что страница входа открывается корректно"""
        response = self.client.get(reverse("registration:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_view_post(self):
        """Проверяет успешный вход пользователя"""
        login_data = {"username": self.user.username, "password": self.user_data["password"]}
        response = self.client.post(reverse("registration:login"), data=login_data)
        self.assertEqual(response.status_code, 302)  # Перенаправление на главную страницу

    def test_logout_view(self):
        """Проверяет успешный выход пользователя"""
        self.client.login(username=self.user.username, password=self.user_data["password"])
        response = self.client.get(reverse("registration:logout"))
        self.assertEqual(response.status_code, 302)  # Перенаправление после выхода
        self.assertNotIn("_auth_user_id", self.client.session)  # Проверка, что пользователь разлогинился

    def test_custom_user_fields(self):
        """Проверяет дополнительные поля модели пользователя"""
        self.assertEqual(self.user.phone, self.user_data["phone"])
        self.assertEqual(self.user.address, self.user_data["address"])
        self.assertEqual(self.user.email, self.user_data["email"])



