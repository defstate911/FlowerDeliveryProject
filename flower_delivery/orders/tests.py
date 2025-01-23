from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Bouquet, Order, OrderItem

User = get_user_model()

class OrderModelTests(TestCase):
    def setUp(self):
        # Создаём пользователя
        self.user = User.objects.create_user(username='testuser', password='password')
        # Создаём букет
        self.bouquet = Bouquet.objects.create(name='Test Bouquet', price=500.00)
        # Создаём заказ
        self.order = Order.objects.create(user=self.user, status='pending')

        # Создаём элемент заказа
        self.order_item = OrderItem.objects.create(order=self.order, bouquet=self.bouquet, quantity=2)

    def test_order_total_cost(self):
        # Проверяем общую стоимость заказа
        total_cost = self.order.get_total_cost()
        self.assertEqual(total_cost, 1000.00)

    def test_order_str(self):
        # Проверяем строковое представление заказа
        self.assertEqual(str(self.order), f"Order {self.order.id} by {self.user.username}")

    def test_order_summary(self):
        # Проверяем текстовый отчёт заказа
        summary = self.order.get_summary()
        self.assertIn("Поступил заказ", summary)
        self.assertIn("Test Bouquet", summary)
        self.assertIn("1000.00 руб.", summary)

class OrderViewTests(TestCase):
    def setUp(self):
        # Создаём пользователя
        self.user = User.objects.create_user(username='testuser', password='password')
        self.bouquet = Bouquet.objects.create(name='Test Bouquet', price=500.00)

    def test_create_order_guest(self):
        # Тест создания заказа гостем
        response = self.client.post(reverse('orders:create_order'), {
            'bouquet_id': self.bouquet.id,
            'quantity': 2,
            'name': 'Гость',
            'email': 'guest@example.com',
            'phone': '1234567890',
            'address': 'Guest Address'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.exists())
        order = Order.objects.first()
        self.assertEqual(order.name, 'Гость')
        self.assertEqual(order.get_total_cost(), 1000.00)

    def test_create_order_authenticated_user(self):
        # Настройка профиля пользователя с телефоном
        self.user.phone = '1234567890'  # Предполагаем, что телефон хранится в связанном профиле
        self.user.save()

        # Авторизация пользователя
        self.client.login(username='testuser', password='password')

        # Создание заказа авторизованным пользователем
        response = self.client.post(reverse('orders:create_order'), {
            'bouquet_id': self.bouquet.id,
            'quantity': 1,
            'address': '123 Flower Street',
        })

        # Проверяем, что запрос успешно завершился редиректом
        self.assertEqual(response.status_code, 302)  # Redirect to order_list

        # Проверяем, что заказ создан
        order = Order.objects.first()
        self.assertIsNotNone(order)  # Заказ должен существовать
        self.assertEqual(order.user, self.user)  # Проверяем, что заказ связан с текущим пользователем
        self.assertEqual(order.get_total_cost(), 500.00)  # Проверяем правильность подсчета стоимости

        # Проверяем, что телефон подгрузился из базы данных
        self.assertEqual(order.phone, '1234567890')  # Телефон должен быть взят из профиля пользователя

    # def test_create_order_authenticated_user(self):
    #     response = self.client.post(reverse('orders:create_order'), {
    #         'field1': 'value1',  # Заполните остальные поля заказа
    #     })
    #
    #     self.assertEqual(response.status_code, 201)  # Или другой ожидаемый статус
    #     self.assertTrue(Order.objects.filter(field1='value1').exists())
    #
    #
    #     # Тест создания заказа авторизованным пользователем
    #     self.client.login(username='testuser', password='password')
    #     response = self.client.post(reverse('orders:create_order'), {
    #         'bouquet_id': self.bouquet.id,
    #         'quantity': 1,
    #         #'phone': '1234567890',  # Добавляем поле phone
    #
    #     })
    #     self.assertEqual(response.status_code, 302)  # Redirect to order_list
    #     order = Order.objects.first()
    #     self.assertEqual(order.user, self.user)
    #     self.assertEqual(order.get_total_cost(), 500.00)
    #     #self.assertEqual(order.phone, '1234567890')  # Проверяем, что телефон сохранен правильно
    #     #self.assertEqual(order.address, 'vvvvvvv')

    def test_order_list_view(self):
        # Тест отображения списка заказов
        self.client.login(username='testuser', password='password')
        Order.objects.create(user=self.user, status='pending')
        response = self.client.get(reverse('orders:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Заказ")
