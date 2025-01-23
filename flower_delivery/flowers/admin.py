from django.contrib import admin  # Импортируем модуль admin
from orders.models import Order, OrderItem  # Правильный импорт после перемещения модели
from flowers.models import Bouquet

# Register your models here.
admin.site.register(Bouquet)
admin.site.register(Order)
admin.site.register(OrderItem)




