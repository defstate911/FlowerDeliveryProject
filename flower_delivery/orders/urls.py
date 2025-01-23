from django.urls import path
from . import views  # Импортируем представления из текущего приложения

app_name = 'orders'  # Пространство имён для маршрутов

urlpatterns = [
    path('', views.order_list, name='order_list'),  # Список заказов
    path('create/', views.create_order, name='create_order'),  # Создание заказа
    #path('guest-order/', views.create_order, name='guest_order'),  # Маршрут для быстрого заказа
    path('order_type_selection/', views.order_type_selection, name='order_type_selection'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),  # Детали заказа
    #path('<int:order_id>/update/', views.update_order, name='update_order'),  # Обновление заказа
    #path('<int:order_id>/delete/', views.delete_order, name='delete_order'),  # Удаление заказа
]
