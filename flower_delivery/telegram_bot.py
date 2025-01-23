import telebot
from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
CHAT_ID = settings.TELEGRAM_CHAT_ID
bot = telebot.TeleBot(BOT_TOKEN)
#print(BOT_TOKEN)
#print(CHAT_ID)

def send_order_notification(order_info):
    """
    Отправляет уведомление в Телеграм.
    :param order_info: информация о заказе (строка или список)
    """
    if isinstance(order_info, (list, tuple)):
        order_message = "\n".join(order_info)
    elif isinstance(order_info, str):
        order_message = order_info
    else:
        order_message = str(order_info)
    try:
        bot.send_message(CHAT_ID, f"Новый заказ!\n{order_message}")
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")

