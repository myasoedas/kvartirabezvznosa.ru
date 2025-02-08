# Сайт риелтора: Карина Дерябина - kvartirabezvznosa.ru

**Сайт kvartirabezvznosa.ru** — это многопользовательское веб-приложение, разработанное на Django 3.2, python 3.9 с лендингом на главной странице (лидогенератором) и блогом риелтора Карина Дерябина - генератором естественного трафика. Приложение предоставляет пользователям возможность получать лиды с лендинга, создавать, редактировать и управлять публикации в блоге, а также взаимодействовать с пользователями через комментарии.

## Подробный гайд по запуску сайта kvartirabezvznosa.ru в продакшен-среде на Ubuntu 22.04 в cloud.ru

### Технологический стек

- **Python**: 3.9
- **Django**: 3.2
- **PostgreSQL**: 12 и выше
- **Gunicorn**: WSGI-сервер для запуска Django
- **Nginx**: Веб-сервер для обработки запросов
- **Ubuntu**: 22.04
- **VSCod**: 22.04

### Требования

- **Операционная система**: Ubuntu 22.04
- **Права суперпользователя (sudo)** для установки пакетов
- **Python 3.9** (или выше)
- **PostgreSQL 12** (или выше)
- **Git** для управления версиями

### Создайте в корне проекта файл .env со следующими переменными:
```python
DATABASE_NAME=usernamebd
DATABASE_USER=username
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432

SECRET_KEY=django-insecure-secret_key

EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=info@yandex.com
EMAIL_HOST_PASSWORD=password

# Подключение бакета cloud.ru
# Параметры аутентификации
AWS_TENANT_ID=9e12c22...2fa665e89
AWS_ACCESS_KEY_ID=34929ade...7235f27c7b516
AWS_SECRET_ACCESS_KEY=1d6173d...d27047e582

# Параметры бакета
AWS_STORAGE_BUCKET_NAME=bucket-name
AWS_S3_ENDPOINT_URL=https://s3.cloud.ru
AWS_S3_REGION_NAME=ru-central-1
AWS_S3_SIGNATURE_VERSION=s3v4

# Если хотите использовать доменное имя вида https://s3.cloud.ru/bucket-name/static/
# сформируйте его из endpoint и имени бакета:
AWS_S3_CUSTOM_DOMAIN=bucket-name.s3.cloud.ru
```

PS: Для подключения к s3 хранилищу cloud.ru необходимо использовать: boto3==1.35.0 
PS: только версия boto3==1.35.0 работает все что новее - работать не будет!

### При установке CKEDITOR 5 текст в поле рекдактирования слишком светлый и его плохо видно на белом фоне. Чтобы исправить эту проблему необходимо найти папку 
```ssh
./venv/lib/django_ckeditor_5/static/dist/style.css
```
### и добавить в конец этого файла код css:

```css
/* Изменение цвета текста внутри области редактирования */
.ck-editor__editable {
    color: black; /* Устанавливаем текст черного цвета */
    background-color: white; /* Устанавливаем фон белым (опционально) */
    font-family: Arial, sans-serif; /* Задаем шрифт текста */
    font-size: 16px; /* Устанавливаем размер шрифта */
}
```

# Инструкция по подключению Django 3.2 к S3‑хранилищу Cloud.ru

Эта инструкция предназначена для среды, где домашний каталог пользователя — **/home/violetta**, а проект располагается в каталоге **/home/violetta/dev/osteopat-violetta**.  
Пример структуры каталогов проекта:

```
/home/violetta/dev/osteopat-violetta/
├── .env
├── policy.json
├── blogicum_project/
│   ├── manage.py
│   ├── upload_static_dev.py
│   ├── static_dev/         # локальные файлы статики для collectstatic
│   └── blogicum/
│       ├── settings.py
│       ├── storage_backends.py
│       └── ... (остальные модули проекта)
```

В данной инструкции описываются следующие этапы:
1. Установка и настройка AWS CLI  
2. Создание и настройка файла переменных окружения (.env)  
3. Настройка Django (settings.py) для работы с Cloud.ru S3  
4. Реализация кастомного storage backend (storage_backends.py)  
5. Применение политики бакета (policy.json) для публичного доступа к статикам  
6. Сбор статики через Django (collectstatic) и тестирование загрузки  
7. Дополнительные рекомендации по отладке, логированию и мерам безопасности

---

## 1. Установка и настройка AWS CLI

### 1.1. Установка AWS CLI

**Для Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install awscli
```

**Через pip (если предпочтительно):**
```bash
pip install awscli
```

**Проверка версии:**
```bash
aws --version
```
_Ожидаемый вывод (пример):_
```
aws-cli/1.22.34 Python/3.10.12 Linux/5.15.0-130-generic botocore/1.23.34
```

### 1.2. Настройка AWS CLI

#### 1.2.1. Файл credentials

**Путь:**  
`/home/violetta/.aws/credentials`

Откройте файл в редакторе (например, vim):
```bash
vim /home/violetta/.aws/credentials
```
Вставьте следующие строки (обратите внимание на формат ключа: tenant_id:key_id):
```ini
[default]
aws_access_key_id = 9e12c22...c7b516
aws_secret_access_key = 1d6173d...27047e582
```

#### 1.2.2. Файл config

**Путь:**  
`/home/violetta/.aws/config`

Откройте файл:
```bash
vim /home/violetta/.aws/config
```
Добавьте:
```ini
[default]
region = ru-central-1
```

#### 1.2.3. Проверка AWS CLI

Запустите команду:
```bash
aws --endpoint-url=https://s3.cloud.ru --region ru-central-1 s3api list-buckets
```
_Ожидаемый вывод (пример):_
```json
{
    "Buckets": [
        {
            "Name": "bucket-violetta",
            "CreationDate": "2025-02-03T07:58:27.978Z"
        }
    ],
    "Owner": {
        "ID": "9e12c2...fa665e89"
    }
}
```
Если появляются ошибки, запустите с флагом `--debug` для подробного логирования.

---

## 2. Файл переменных окружения (.env)

**Путь:**  
`/home/violetta/dev/osteopat-violetta/.env`

Создайте или отредактируйте файл с таким содержимым:

```ini
# Настройки базы данных
DATABASE_NAME=violettabd
DATABASE_USER=violetta
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Секретный ключ Django
SECRET_KEY=djang...ubjp(&79w1

# Настройки почты через SMTP Яндекса
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=info@yandex.com
EMAIL_HOST_PASSWORD=password

# Параметры аутентификации для Cloud.ru S3
AWS_TENANT_ID=9e12...fa665e89
AWS_ACCESS_KEY_ID=3492...c7b516
AWS_SECRET_ACCESS_KEY=1d61...047e582

# Параметры бакета Cloud.ru
AWS_STORAGE_BUCKET_NAME=bucket-username
AWS_S3_ENDPOINT_URL=https://s3.cloud.ru
AWS_S3_REGION_NAME=ru-central-1
AWS_S3_SIGNATURE_VERSION=s3v4

# Домен для доступа к статикам (виртуальный хостинг Cloud.ru)
AWS_S3_CUSTOM_DOMAIN=bucket-username.s3.cloud.ru
```

> **Замечание по безопасности:**  
> Файл .env содержит конфиденциальную информацию. Убедитесь, что он не публикуется в общедоступных репозиториях и имеет корректные права доступа.

---

## 3. Настройка Django (settings.py)

**Путь:**  
`/home/violetta/dev/osteopat-violetta/blogicum_project/blogicum/settings.py`

Ниже приведён фрагмент, отвечающий за интеграцию с Cloud.ru S3:

```python
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent  # /home/violetta/dev/osteopat-violetta/blogicum_project

SECRET_KEY = config('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'osteopatvioletta.ru',
    'www.osteopatvioletta.ru',
    'osteopat-violetta.ru',
    'www.osteopat-violetta.ru',
]

# ... (остальные стандартные настройки: INSTALLED_APPS, MIDDLEWARE, TEMPLATES, DATABASES, EMAIL и пр.)

# ------------------------------------------------------------------------------
# Настройки для работы со статиками через Cloud.ru S3

AWS_TENANT_ID = config('AWS_TENANT_ID')
# Формирование ключа доступа: tenant_id:key_id
AWS_ACCESS_KEY_ID = f"{AWS_TENANT_ID}:{config('AWS_ACCESS_KEY_ID')}"
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION = config('AWS_S3_SIGNATURE_VERSION')
AWS_S3_ADDRESSING_STYLE = "path"

AWS_S3_CONFIG = {
    "s3": {"addressing_style": "path"},
    "signature_version": "s3v4",
}

AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')

STATICFILES_STORAGE = "blogicum.storage_backends.StaticStorage"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_dev')]
```

Ключевые моменты:  
- Ключ доступа формируется как `tenant_id:key_id`  
- STATIC_URL указывает на виртуальный хостинг:  
  `https://bucket-violetta.s3.cloud.ru/static/`

---

## 4. Кастомный Storage Backend

**Путь:**  
`/home/violetta/dev/osteopat-violetta/blogicum_project/blogicum/storage_backends.py`

Создайте файл со следующим содержимым:

```python
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from botocore.client import Config

class StaticStorage(S3Boto3Storage):
    # Все файлы статики будут загружаться в бакете в папку "static"
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True

    def connection_params(self):
        params = super().connection_params() or {}
        params.update({"config": Config(**settings.AWS_S3_CONFIG)})
        return params
```

---

## 5. Политика бакета (Bucket Policy)

**Путь:**  
`/home/violetta/dev/osteopat-violetta/policy.json`

Создайте файл с таким содержимым:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadStatic",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::bucket-violetta/static/*"
    }
  ]
}
```

### Применение политики:

Откройте терминал и выполните:
```bash
aws --profile default --endpoint-url=https://s3.cloud.ru s3api put-bucket-policy --bucket bucket-violetta --policy file://policy.json
```
Проверить применение можно:
```bash
aws --profile default --endpoint-url=https://s3.cloud.ru s3api get-bucket-policy --bucket bucket-violetta
```

---

## 6. Сбор статики через Django

Перейдите в каталог проекта и выполните сбор статики:
```bash
cd /home/violetta/dev/osteopat-violetta/blogicum_project
python manage.py collectstatic
```
Эта команда соберёт файлы из директории `/home/violetta/dev/osteopat-violetta/blogicum_project/static_dev` и загрузит их в бакет Cloud.ru в папку `static`.

---

## 7. Проверка доступа к статике

Откройте в браузере URL, например:
```
https://bucket-violetta.s3.cloud.ru/static/robots.txt
```
Если файл отображается корректно, значит настройка выполнена успешно.

---

## 8. Тестовая утилита загрузки файлов (upload_static_dev.py)

**Путь:**  
`/home/violetta/dev/osteopat-violetta/blogicum_project/upload_static_dev.py`

Создайте файл с следующим содержимым:

```python
import os
import boto3
import mimetypes
from botocore.client import Config

# 🔹 Конфигурация S3 для теста
AWS_TENANT_ID = "9e12c2...fa665e89"
AWS_ACCESS_KEY_ID = "3492...b516"
AWS_SECRET_ACCESS_KEY = "1d61...47e582"
AWS_S3_ENDPOINT_URL = "https://s3.cloud.ru"
AWS_S3_REGION_NAME = "ru-central-1"
AWS_BUCKET_NAME = "bucket-violetta"

session = boto3.session.Session()
s3 = session.client(
    "s3",
    aws_access_key_id=f"{AWS_TENANT_ID}:{AWS_ACCESS_KEY_ID}",
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=AWS_S3_ENDPOINT_URL,
    region_name=AWS_S3_REGION_NAME,
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "path"},
        request_checksum_calculation='when_required',
        response_checksum_validation='when_required',
    )
)

try:
    response = s3.list_buckets()
    print("✅ Доступные бакеты:", [bucket["Name"] for bucket in response["Buckets"]])
except Exception as e:
    print("🛑 Ошибка подключения к S3:", e)
    exit(1)

LOCAL_STATIC_DIR = "static_dev"
S3_STATIC_PREFIX = "static"

print(f"🚀 Начинаем загрузку файлов из '{LOCAL_STATIC_DIR}' в S3 бакет '{AWS_BUCKET_NAME}/{S3_STATIC_PREFIX}'")

if not os.path.exists(LOCAL_STATIC_DIR):
    print(f"🛑 Ошибка: Папка '{LOCAL_STATIC_DIR}' не найдена!")
    exit(1)

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type if mime_type else "application/octet-stream"

for root, _, files in os.walk(LOCAL_STATIC_DIR):
    for file_name in files:
        local_path = os.path.join(root, file_name)
        s3_path = os.path.relpath(local_path, LOCAL_STATIC_DIR)
        s3_key = f"{S3_STATIC_PREFIX}/{s3_path}"
        try:
            s3.upload_file(
                local_path,
                AWS_BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    "ContentType": get_mime_type(local_path),
                    "CacheControl": "max-age=86400",
                }
            )
            print(f"✅ Успешно загружен: {s3_key}")
        except Exception as e:
            print(f"🛑 Ошибка загрузки {s3_key}: {e}")

print("🎉 Загрузка завершена!")
```

Запустите утилиту:
```bash
cd /home/violetta/dev/osteopat-violetta/blogicum_project
python upload_static_dev.py
```

---

## 9. Рекомендации по отладке и безопасности

- **Отладка:**  
  Если возникают ошибки, используйте флаг `--debug` в AWS CLI или увеличьте уровень логирования в Django (например, добавив `logging.basicConfig(level=logging.DEBUG)`), чтобы получить подробную информацию о запросах.
  
- **Проверка переменных:**  
  Используйте небольшой Python‑скрипт для проверки значений переменных из .env (например, `check_creds.py`), чтобы убедиться, что все параметры корректно считываются.
  
- **Безопасность:**  
  Не публикуйте файлы `.env`, `~/.aws/credentials` и другие конфиденциальные данные в общедоступных репозиториях. Установите соответствующие права доступа на эти файлы.

---

# Заключение

Эта инструкция содержит все необходимые этапы для подключения вашего Django‑приложения к S3‑хранилищу от Cloud.ru, включая установку и настройку AWS CLI, настройку переменных окружения, конфигурацию Django, создание кастомного storage backend, применение политики бакета, сбор статики и тестирование загрузки файлов. Если возникнут вопросы или потребуется дополнительная настройка, используйте логирование и отладочные команды для диагностики, а также обращайтесь за поддержкой.

