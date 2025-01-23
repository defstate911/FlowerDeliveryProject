from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, Bouquet  # Импорты моделей
from django.contrib.auth.decorators import login_required
from telegram_bot import send_order_notification  # Импорт функции отправки уведомления из бота

def get_user_from_session(request):
    return request.user

def get_bouquet(bouquet_id):
    return get_object_or_404(Bouquet, id=bouquet_id)

def create_order_sync(**kwargs):
    return Order.objects.create(**kwargs)

def create_order_item(order, bouquet, quantity):
    return OrderItem.objects.create(order=order, bouquet=bouquet, quantity=quantity)


def create_order(request):
    if request.method == 'POST':
        bouquet_id = request.POST.get('bouquet_id')
        if not bouquet_id or not bouquet_id.isdigit():
            return redirect('flowers:home')

        bouquet = get_object_or_404(Bouquet, id=int(bouquet_id))
        quantity = int(request.POST.get('quantity', 1))

        if not request.user.is_authenticated:  # Гостевой заказ
            name = request.POST.get('name', 'Гость')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get('address', '')

            # Создаем гостевой заказ
            order = Order.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address
            )
        else:  # Заказ от зарегистрированного пользователя
            user = request.user
            phone = getattr(user, 'phone', None)
            address = request.POST.get('address', getattr(user, 'address', ''))

            # Создаем заказ для зарегистрированного пользователя
            order = Order.objects.create(
                user=user,
                name=user.get_full_name(),
                email=user.email,
                phone=phone,
                address=address
            )

        # Создаем OrderItem
        OrderItem.objects.create(order=order, bouquet=bouquet, quantity=quantity)

        # Отправляем уведомление в Telegram
        order_summary = order.get_summary()
        send_order_notification(order_summary)

        # Перенаправление на страницу подтверждения заказа

        # Перенаправление на разные страницы для гостей и пользователей
        if request.user.is_authenticated:
            return redirect('orders:order_list')  # Для зарегистрированных пользователей
        else:
            return render(request, 'orders/guest_order_summary.html', {'order': order})

        #return render(request, 'orders/guest_order_summary.html', {'order': order})

    # Если запрос GET
    bouquet_id = request.GET.get('bouquet_id')
    if bouquet_id:
        selected_bouquet = get_object_or_404(Bouquet, id=int(bouquet_id))
        if not request.user.is_authenticated:
            return render(request, 'orders/guest_order.html', {'selected_bouquet': selected_bouquet})
        else:
            return render(request, 'orders/create_order.html', {'selected_bouquet': selected_bouquet})

    return redirect('flowers:home')

def order_type_selection(request):
     bouquet_id = request.GET.get('bouquet_id')  # Получить id букета из параметров запроса
     return render(request, 'orders/order_type_selection.html', {'bouquet_id': bouquet_id})

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect('orders:order_detail', order_id=order.id)
    return render(request, 'orders/update_order.html', {'order': order})

# @login_required
# def delete_order(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     order.delete()
#     return redirect('orders:order_list')


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

