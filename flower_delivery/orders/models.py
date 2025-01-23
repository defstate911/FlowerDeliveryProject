from django.db import models
from django.contrib.auth.models import User
from flowers.models import Bouquet
from django.conf import settings

class Order(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)  # Связь с пользователем, необязательна для гостевых заказов
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    bouquets = models.ManyToManyField(Bouquet, related_name='orders', through='OrderItem')  # Связь с букетами через промежуточную таблицу
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания заказа
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления заказа

    # Поля для гостевых заказов
    name = models.CharField(max_length=100, blank=True)  # Имя гостя
    email = models.EmailField(blank=True)  # Почта гостя
    phone = models.CharField(max_length=15, blank=True)  # Телефон гостя
    address = models.TextField(blank=True)  # Адрес гостя

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В обработке'),
            ('completed', 'Завершён'),
            ('canceled', 'Отменён')
        ],
        default='pending'
    )  # Статус заказа

    def get_total_cost(self):
        return sum(item.total_price for item in self.items.all())

    def get_summary(self):
        """
        Возвращает текстовый отчёт о заказе (подходит как для гостей, так и для авторизованных пользователей).
        """
        total_price = sum(item.bouquet.price * item.quantity for item in self.items.all())
        bouquets = ', '.join([f"{item.bouquet.name} (x{item.quantity})" for item in self.items.all()])

        # Добавляем информацию о заказчике
        customer_info = f"""Имя заказчика: {self.name or self.user or (self.user.get_full_name() if self.user else 'Не указано')}
        Телефон: {self.phone or 'Не указан'}
        Адрес: {self.address or 'Не указан'}"""

        
        if self.user:  # Если заказ связан с зарегистрированным пользователем
            #print(
                #f"DEBUG: user={self.user}, name={self.name}, full_name={self.user.get_full_name() if self.user else None}")
            return f"Поступил заказ №{self.id}. Букеты: {bouquets}. Общая сумма: {total_price} руб. {customer_info}"
        else:  # Если заказ оформлен гостем
            return f"Поступил заказ №{self.id}. Букеты: {bouquets}. Общая сумма: {total_price} руб. {customer_info}"

    def __str__(self):
        if self.user:
            return f"Order {self.id} by {self.user.username}"
        return f"Order {self.id} (Guest: {self.name})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Связь с заказом
    bouquet = models.ForeignKey(Bouquet, related_name='order_items', on_delete=models.CASCADE)  # Связь с букетом
    quantity = models.PositiveIntegerField(default=1)  #


    @property
    def total_price(self):
        # Возвращаем цену букета умноженную на количество
        return self.bouquet.price * self.quantity