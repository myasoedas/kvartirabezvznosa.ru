import django
import os
import sys
from django.core.mail import send_mail
from django.conf import settings

# Установите путь к корневой директории проекта (где находится manage.py)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(project_root)

# Укажите путь к файлу настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogicum.settings")

# Инициализация Django
django.setup()

# Отправка тестового письма
try:
    send_mail(
        'Тестовое сообщение',
        'Это тестовое сообщение для проверки подключения к почтовому серверу Яндекс.',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],  # Отправляем на тот же адрес, который указан в EMAIL_HOST_USER
        fail_silently=False,
    )
    print("Тестовое письмо успешно отправлено!")
except Exception as e:
    print("Ошибка при отправке письма:", e)
