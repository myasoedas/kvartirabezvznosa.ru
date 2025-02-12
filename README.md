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

---

### Краткий обзор основных компонентов проекта:

---

### 1. Основные папки и файлы

- **.github/workflows/**  
  Здесь находятся файлы GitHub Actions, отвечающие за автоматизацию (CI/CD, деплой и т.д.). Это позволяет тебе запускать тесты, сборку Docker-образов и деплой на сервер по push в репозиторий.

- **blogicum_project/**  
  Главная директория проекта на Django. В ней располагаются файлы управления (manage.py), настройки (settings.py), а также дополнительные скрипты, такие как upload_static_dev.py для загрузки статики в S3‑хранилище Cloud.ru. Помимо этого, внутри находятся модули самого приложения (например, blogicum).

- **nginx/conf.d/**  
  Конфигурационные файлы для Nginx, которые используются для настройки обратного прокси, SSL‑терминации и маршрутизации запросов к приложению.

- **tests/**  
  Папка с тестами, где, вероятно, содержатся юнит‑тесты или интеграционные тесты для проверки корректности работы приложения.

- **.env.example**  
  Пример файла с переменными окружения, содержащий настройки для подключения к базе данных, почтовому серверу, AWS/Cloud.ru S3 и другие параметры. Этот файл помогает правильно настроить локальное или продакшн‑окружение, не раскрывая реальные секреты.

- **.gitignore**  
  Файл, в котором указаны файлы и директории, исключаемые из системы контроля версий (например, конфиденциальные настройки, venv, кеши и т.п.).

- **Dockerfile**  
  Скрипт для сборки Docker‑образа приложения. Он описывает этапы сборки твоего Django‑проекта, что важно для создания стабильного продакшн‑окружения.

- **docker-compose.yml**  
  Файл для оркестрации нескольких Docker‑контейнеров (например, для приложения, базы данных, Nginx и т.д.). Это позволяет тебе легко запускать весь стек локально или на сервере.

- **requirements.txt**  
  Список зависимостей Python, необходимых для работы проекта. Здесь указаны версии Django, библиотеки для работы с PostgreSQL, а также прочие модули, включая зависимости для интеграции с S3 (boto3 и т.п.).

- **setup.cfg**  
  Конфигурационный файл для настройки параметров сборки, тестирования или линтинга проекта. Он помогает поддерживать стандарты кода и автоматизировать проверки.

- **README.md**  
  Подробная инструкция по запуску и деплою сайта. В нём описан стек технологий, настройка переменных окружения, интеграция с S3‑хранилищем Cloud.ru, а также пошаговые рекомендации по установке и настройке окружения (на примере Ubuntu 22.04).

- **LICENSE**  
  Файл с информацией о лицензировании проекта.

---

### 2. Ключевые особенности проекта

- **Django 3.2 и Python 3.9**  
  Проект построен на стабильной версии Django, с подробными инструкциями по деплою и настройке, в том числе для интеграции с облачным хранилищем Cloud.ru.

- **Интеграция с Cloud.ru S3**  
  В проекте реализована настройка для хранения статики через S3‑хранилище Cloud.ru. Для этого настроен кастомный storage backend (`storage_backends.py`), а также есть инструкция по настройке AWS CLI и загрузке статики.

- **Контейнеризация**  
  Использование Docker и docker-compose позволяет создавать воспроизводимые окружения как для разработки, так и для продакшена.

- **CI/CD**  
  Файлы GitHub Actions в папке `.github/workflows` автоматизируют сборку, тестирование и деплой проекта.

---

Ниже приведена обновлённая подробная инструкция по созданию и настройке общего SSL‑сертификата от Let's Encrypt для доменов:

- kvartirabezvznosa.ru  
- www.kvartirabezvznosa.ru  
- bezvznosa.ru  
- www.bezvznosa.ru  
- ipotekabezvznosa.ru  
- www.ipotekabezvznosa.ru

при условии, что твои сервисы (Django 3.2 с Gunicorn, Nginx‑proxy и Certbot‑companion) работают в отдельных Docker‑контейнерах. Инструкция учитывает твои рабочие файлы.

---

## Шаг 1. Предварительные условия

1. **DNS‑записи**  
   Убедись, что для всех указанных доменов (как с www, так и без) настроены корректные A‑записи, которые указывают на IP твоего VPS. Только так ACME‑валидация сможет пройти успешно.

2. **Структура проекта**  
   В корне проекта (например, `/path/to/kvartirabezvznosa.ru`) должны располагаться следующие файлы и каталоги:
   
   ```
   /path/to/kvartirabezvznosa.ru/
   ├── docker-compose.yml
   ├── Dockerfile
   ├── .env
   ├── nginx/
   │   ├── conf.d/
   │   │   └── default.conf        <-- твой конфиг, описанный ниже
   │   ├── vhost.d/              <-- для виртуальных хостов (можно оставить пустой)
   │   └── html/                 <-- статичные HTML-страницы (например, для ошибок)
   └── certbot/
       ├── conf/                 <-- для конфигурационных файлов и сертификатов
       └── www/                  <-- для файлов ACME‑challenge
   ```
   
   Создать папки для Certbot можно командой:
   
   ```bash
   mkdir -p /path/to/kvartirabezvznosa.ru/certbot/conf /path/to/kvartirabezvznosa.ru/certbot/www
   ```

---

## Шаг 2. Настройка файла Dockerfile и docker-compose.yml

Используй следующий обновлённый вариант `Dockerfile`:
```
# Используем официальный образ Python 3.9-slim
FROM python:3.9-slim

# Отключаем буферизацию вывода для корректного логирования
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код в контейнер
COPY . /app/

# Создаем папку логов
RUN mkdir -p /app/blogicum_project/logs && touch /app/blogicum_project/logs/django_debug.log

# Устанавливаем PYTHONPATH, чтобы можно было импортировать blogicum
ENV PYTHONPATH=/app/blogicum_project

# Запускаем Gunicorn с 3 воркерами
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "blogicum_project.blogicum.wsgi:application"]

```
---

Используй следующий обновлённый вариант `docker-compose.yml`:

```yml
version: "3.9"

services:
  nginx-proxy:
    image: jwilder/nginx-proxy
    container_name: nginx_proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      # Для получения информации о запущенных контейнерах
      - /var/run/docker.sock:/tmp/docker.sock:ro
      # Здесь будут храниться сертификаты, генерируемые Let's Encrypt
      - certbot_certs:/etc/nginx/certs:ro
      # Дополнительные конфиги для виртуальных хостов (папку можно создать пустой)
      - ./nginx/vhost.d:/etc/nginx/vhost.d:ro
      # Статические HTML-страницы (например, для ошибок)
      - ./nginx/html:/usr/share/nginx/html
    networks:
      - app_net

  letsencrypt:
    image: jrcs/letsencrypt-nginx-proxy-companion
    container_name: nginx_letsencrypt
    restart: always
    environment:
      - NGINX_PROXY_CONTAINER=nginx_proxy
      - LETSENCRYPT_REFRESH_INTERVAL=3600
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
      - ./nginx/vhost.d:/etc/nginx/vhost.d:rw
      - ./nginx/html:/usr/share/nginx/html:rw
      - certbot_certs:/etc/nginx/certs:rw
    depends_on:
      - nginx-proxy
    networks:
      - app_net

  web:
    build: .
    container_name: django_app
    command: gunicorn --workers 3 --bind 0.0.0.0:8000 blogicum_project.blogicum.wsgi:application
    env_file:
      - .env
    environment:
      # Указываем домены, по которым будет доступно приложение,
      # и для которых будет запрошен сертификат
      - VIRTUAL_HOST=kvartirabezvznosa.ru,www.kvartirabezvznosa.ru,bezvznosa.ru,www.bezvznosa.ru,ipotekabezvznosa.ru,www.ipotekabezvznosa.ru
      - LETSENCRYPT_HOST=kvartirabezvznosa.ru,www.kvartirabezvznosa.ru,bezvznosa.ru,www.bezvznosa.ru,ipotekabezvznosa.ru,www.ipotekabezvznosa.ru
      - LETSENCRYPT_EMAIL=myasoedas@yandex.ru
      - VIRTUAL_PORT=8000
    volumes:
      - .:/app
      - ./logs:/app/blogicum_project/logs
      - ./media:/app/media
    depends_on:
      - db
    networks:
      - app_net

  db:
    image: postgres:15
    container_name: postgres_db
    restart: always
    env_file:
      - .env
    environment:
      - POSTGRES_DB=${DATABASE_NAME}
      - POSTGRES_USER=${DATABASE_USER}
      - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_net

networks:
  app_net:
    driver: bridge

volumes:
  postgres_data:
  certbot_certs:

```

**Пояснения:**  
- **nginx-proxy** использует именованный volume `certbot_certs` для сертификатов (сертификаты будут храниться в этом volume и монтироваться в `/etc/nginx/certs` внутри контейнера).  
- **letsencrypt** (образ jrcs/letsencrypt-nginx-proxy-companion) использует тома `./certbot/conf` и `./certbot/www` для сохранения конфигурации и для ACME‑challenge.  
- **web** (твой Django‑приложение) имеет переменные окружения VIRTUAL_HOST, LETSENCRYPT_HOST и LETSENCRYPT_EMAIL, которые companion‑контейнер использует для запроса сертификатов для всех доменов.

---

## Шаг 3. Настройка Nginx конфигурации

Создайте в корне проекта папки: 
nginx/conf.d/
nginx/vhost.d/
nginx/html/

certbot/conf/
certbot/www/


В файле `nginx/conf.d/default.conf` размести следующую конфигурацию (как ты уже сделал на VPS):

```nginx
#################################################################
# HTTP: Обработка ACME-челленджа и редирект всех запросов на HTTPS
#################################################################
server {
    listen 80;
    server_name kvartirabezvznosa.ru www.kvartirabezvznosa.ru bezvznosa.ru www.bezvznosa.ru ipotekabezvznosa.ru www.ipotekabezvznosa.ru;

    # Обработка ACME-челленджа для Certbot (используется для получения и продления сертификатов)
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri =404;
    }

    # Редирект всех остальных запросов с HTTP на HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

#################################################################
# HTTPS: Основной блок для обслуживания запросов с SSL
#################################################################
server {
    listen 443 ssl http2;
    server_name kvartirabezvznosa.ru www.kvartirabezvznosa.ru bezvznosa.ru www.bezvznosa.ru ipotekabezvznosa.ru www.ipotekabezvznosa.ru;

    # SSL сертификаты (убеди­сь, что сертификат покрывает все домены)
    ssl_certificate /etc/letsencrypt/live/kvartirabezvznosa.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kvartirabezvznosa.ru/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Обработка favicon – отключаем логирование для уменьшения лишних записей
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    # Проксирование запросов к статикам, которые хранятся на S3
    location /static/ {
        proxy_pass https://s3.cloud.ru/kvartirabezvznosa/static/;
        proxy_set_header Host s3.cloud.ru;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Отдача медиафайлов, которые находятся в контейнере Django
    location /media/ {
        alias /app/media/;
    }

    # Проксирование всех остальных запросов к приложению Django
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

**Замечания:**  
- Директива `root /var/www/certbot;` в блоке ACME‑challenge соответствует тому, куда монтируется папка `./certbot/www` (в контейнере letsencrypt – `/var/www/certbot`).  
- Пути к сертификатам в блоке HTTPS настроены так, что сертификат, сформированный для основного домена `kvartirabezvznosa.ru`, будет применён. При запросе сертификата companion‑контейнер объединит все домены из переменной LETSENCRYPT_HOST в один сертификат.

---

## Шаг 4. Сборка и запуск контейнеров

Создайте в корне проекта файл:
.github/workflow/deploy.yml

```yml
name: Deploy to VPS

on:
  push:
    branches:
      - main  # Автоматический деплой при каждом пуше в ветку main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      # (Опционально: добавьте шаги тестирования или сборки)

      - name: Generate .env file and Deploy via SSH
        uses: appleboy/ssh-action@v0.1.8
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          port: ${{ secrets.VPS_SSH_PORT }}
          script: |
            cd /home/karina/kvartirabezvznosa   # Убедитесь, что этот путь совпадает с расположением репозитория на VPS
            echo "Генерируем файл .env из секретов..."
            cat > .env <<EOF
            DATABASE_NAME=${{ secrets.DATABASE_NAME }}
            DATABASE_USER=${{ secrets.DATABASE_USER }}
            DATABASE_PASSWORD=${{ secrets.DATABASE_PASSWORD }}
            DATABASE_HOST=db
            DATABASE_PORT=5432
            SECRET_KEY=${{ secrets.SECRET_KEY }}
            EMAIL_HOST=${{ secrets.EMAIL_HOST }}
            EMAIL_PORT=${{ secrets.EMAIL_PORT }}
            EMAIL_USE_SSL=${{ secrets.EMAIL_USE_SSL }}
            EMAIL_HOST_USER=${{ secrets.EMAIL_HOST_USER }}
            EMAIL_HOST_PASSWORD=${{ secrets.EMAIL_HOST_PASSWORD }}
            AWS_TENANT_ID=${{ secrets.AWS_TENANT_ID }}
            AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }}
            AWS_STORAGE_BUCKET_NAME=${{ secrets.AWS_STORAGE_BUCKET_NAME }}
            AWS_S3_ENDPOINT_URL=${{ secrets.AWS_S3_ENDPOINT_URL }}
            AWS_S3_REGION_NAME=${{ secrets.AWS_S3_REGION_NAME }}
            AWS_S3_SIGNATURE_VERSION=${{ secrets.AWS_S3_SIGNATURE_VERSION }}
            AWS_S3_CUSTOM_DOMAIN=${{ secrets.AWS_S3_CUSTOM_DOMAIN }}
            EOF

            echo ".env создан. Обновляем код и запускаем контейнеры..."
            git pull origin main
            docker-compose pull
            docker-compose up -d --build

```

Этот файл нужен для автоматического деплоя Github Actions в ваш VPS сервер.

Настройте файл settings.py вашего веб проекта:

```py
import os
from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [
    "kvartirabezvznosa.ru",
    "www.kvartirabezvznosa.ru",
    "bezvznosa.ru",
    "www.bezvznosa.ru",
    "ipotekabezvznosa.ru",
    "www.ipotekabezvznosa.ru",
]

INSTALLED_APPS = [
    # стандартные приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # сторонние приложения
    'django_bootstrap5',
    'django_cleanup.apps.CleanupConfig',
    'django_ckeditor_5',
    'django.contrib.sitemaps',
    'storages',
    # ваши приложения
    'pages.apps.PagesConfig',
    'blog.apps.BlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Путь для загрузки файлов, включая видео
CKEDITOR_UPLOAD_PATH = "uploads/"

# Привязка загруженных файлов к пользователю
CKEDITOR_RESTRICT_BY_USER = False

# Разрешение на загрузку любых файлов, не только изображений
CKEDITOR_ALLOW_NONIMAGE_FILES = True

# Конфигурация CKEditor
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|', 'bold', 'italic', 'underline', 'strikethrough', 'link', '|',
            'bulletedList', 'numberedList', 'blockQuote', '|', 'alignment', '|',
            'imageUpload', 'insertImage', 'mediaEmbed', '|',
            'undo', 'redo', '|', 'fontSize', 'fontFamily', 'highlight', '|',
            'insertTable', 'tableColumn', 'tableRow', 'mergeTableCells', '|',
            'horizontalLine', 'specialCharacters', 'sourceEditing'
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative', 'imageStyle:full', 'imageStyle:side',
                'linkImage'
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells'
            ]
        },
        'mediaEmbed': {
            'previewsInData': True
        },
        'height': 500,  # Adjust editor height
        'width': 'auto',  # Adjust editor width
    }
}

ROOT_URLCONF = 'blogicum.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogicum.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),

    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

handler404 = 'pages.views.custom_404_view'
handler403 = 'pages.views.custom_403_view'
handler500 = 'pages.views.custom_500_view'

LANGUAGE_CODE = 'ru-RU'

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/auth/login/'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Настройка аутентификации для Cloud.ru S3
AWS_TENANT_ID = config('AWS_TENANT_ID')
# Формат tenant_id:key_id
AWS_ACCESS_KEY_ID = f"{AWS_TENANT_ID}:{config('AWS_ACCESS_KEY_ID')}"  
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION = config('AWS_S3_SIGNATURE_VERSION')
# обязательно для Cloud.ru
AWS_S3_ADDRESSING_STYLE = "path"  

# Дополнительные параметры для boto3 (если требуется версия 1.36+)
AWS_S3_CONFIG = {
    #"request_checksum_calculation": "when_required",
    #"response_checksum_validation": "when_required",
    "s3": {"addressing_style": "path"},
    "signature_version": "s3v4",
}

# Формирование домена для доступа к статике
# Если вы хотите, чтобы URL файлов имели вид:
# https://s3.cloud.ru/kvartirabezvznosa/static/...
# можно использовать значение из .env (AWS_S3_CUSTOM_DOMAIN), либо сформировать его:
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_S3_ENDPOINT_URL.replace('https://', '')}/{AWS_STORAGE_BUCKET_NAME}"
AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN')


# Указываем кастомный storage backend для статики
STATICFILES_STORAGE = "blogicum.storage_backends.StaticStorage"

# URL для доступа к статическим файлам
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"

# Пути для локальной статики
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_dev'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# STATICFILES_DIRS = [
#   BASE_DIR / 'static_dev',
# ]

# STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для отправки почты через SMTP Яндекса
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Добавляем таймауты для повышения надежности
EMAIL_TIMEOUT = 10  # Таймаут для подключения (в секундах)

# Добавляем обработку ошибок при сбоях отправки почты
EMAIL_USE_LOCALTIME = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',  # 'INFO' 'WARNING' 'DEBUG' 
            'propagate': True,
        },
    },
}

```

---

### Проверка получения и установкеи бесплатных SSL сертификатов

Ниже приведена подробная инструкция по получению и установке бесплатного SSL‑сертификата для веб‑приложения на Django 3.2, размещённого в Docker‑контейнерах, с использованием автоматического решения от Let’s Encrypt через контейнеры nginx‑proxy и letsencrypt‑nginx‑proxy‑companion.

---

## Шаг 1. Подготовка файлов проекта

### Dockerfile для Django‑приложения

Убедись, что твой Dockerfile выглядит примерно так:

```dockerfile
# Используем официальный образ Python 3.9-slim
FROM python:3.9-slim

# Отключаем буферизацию вывода для корректного логирования
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код в контейнер
COPY . /app/

# Создаем папку логов
RUN mkdir -p /app/blogicum_project/logs && touch /app/blogicum_project/logs/django_debug.log

# Устанавливаем PYTHONPATH, чтобы можно было импортировать blogicum
ENV PYTHONPATH=/app/blogicum_project

# Запускаем Gunicorn с 3 воркерами на порту 8000
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "blogicum_project.blogicum.wsgi:application"]
```

### docker-compose.yml

Файл docker-compose.yml должен содержать описание следующих сервисов:

- **nginx-proxy:**  
  Использует образ `jwilder/nginx-proxy` для автоматического формирования конфигураций на основе переменных окружения, монтирует Docker socket и том для сертификатов.

- **letsencrypt:**  
  Использует образ `jrcs/letsencrypt-nginx-proxy-companion`, который взаимодействует с nginx‑proxy для получения сертификатов у Let’s Encrypt. Здесь обязательно нужно задать переменную `NGINX_PROXY_CONTAINER` (со значением имени контейнера nginx‑proxy) и примонтировать том для сертификатов с правами записи.

- **web:**  
  Сервис с твоим Django‑приложением, который запускается с помощью gunicorn на порту 8000. Здесь задаются переменные окружения для генерации сертификатов – `VIRTUAL_HOST`, `LETSENCRYPT_HOST`, `LETSENCRYPT_EMAIL` и `VIRTUAL_PORT`.

- **db:**  
  Контейнер с PostgreSQL.

Пример файла:

```yaml
version: "3.9"

services:
  nginx-proxy:
    image: jwilder/nginx-proxy
    container_name: nginx_proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
      # Здесь будут храниться сертификаты, полученные от Let’s Encrypt
      - certbot_certs:/etc/nginx/certs:ro
      - ./nginx/vhost.d:/etc/nginx/vhost.d:ro
      - ./nginx/html:/usr/share/nginx/html
    networks:
      - app_net

  letsencrypt:
    image: jrcs/letsencrypt-nginx-proxy-companion
    container_name: nginx_letsencrypt
    restart: always
    environment:
      - NGINX_PROXY_CONTAINER=nginx_proxy
      # В продакшене обычно интервал проверки оставляют 3600 секунд (1 час)
      - LETSENCRYPT_REFRESH_INTERVAL=3600
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
      - ./nginx/vhost.d:/etc/nginx/vhost.d:rw
      - ./nginx/html:/usr/share/nginx/html:rw
      - certbot_certs:/etc/nginx/certs:rw
    depends_on:
      - nginx-proxy
    networks:
      - app_net

  web:
    build: .
    container_name: django_app
    command: gunicorn --workers 3 --bind 0.0.0.0:8000 blogicum_project.blogicum.wsgi:application
    env_file:
      - .env
    environment:
      # Домены, по которым будет доступно приложение и для которых будет получен сертификат:
      - VIRTUAL_HOST=kvartirabezvznosa.ru,www.kvartirabezvznosa.ru,bezvznosa.ru,www.bezvznosa.ru,ipotekabezvznosa.ru,www.ipotekabezvznosa.ru
      - LETSENCRYPT_HOST=kvartirabezvznosa.ru,www.kvartirabezvznosa.ru,bezvznosa.ru,www.bezvznosa.ru,ipotekabezvznosa.ru,www.ipotekabezvznosa.ru
      - LETSENCRYPT_EMAIL=myasoedas@yandex.ru   # Используй свой реальный email
      - VIRTUAL_PORT=8000
    volumes:
      - .:/app
      - ./logs:/app/blogicum_project/logs
      - ./media:/app/media
    depends_on:
      - db
    networks:
      - app_net

  db:
    image: postgres:15
    container_name: postgres_db
    restart: always
    env_file:
      - .env
    environment:
      - POSTGRES_DB=${DATABASE_NAME}
      - POSTGRES_USER=${DATABASE_USER}
      - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_net

networks:
  app_net:
    driver: bridge

volumes:
  postgres_data:
  certbot_certs:
```

### Конфигурация Nginx (default.conf)

Пример файла default.conf (этот файл используется nginx‑proxy или его auto‑генерация companion’ом):

```nginx
#################################################################
# HTTP: Обработка ACME-челленджа и редирект всех запросов на HTTPS
#################################################################
server {
    listen 80;
    server_name kvartirabezvznosa.ru www.kvartirabezvznosa.ru bezvznosa.ru www.bezvznosa.ru ipotekabezvznosa.ru www.ipotekabezvznosa.ru;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri =404;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

#################################################################
# HTTPS: Основной блок для обслуживания запросов с SSL
#################################################################
server {
    listen 443 ssl http2;
    server_name kvartirabezvznosa.ru www.kvartirabezvznosa.ru bezvznosa.ru www.bezvznosa.ru ipotekabezvznosa.ru www.ipotekabezvznosa.ru;

    ssl_certificate /etc/letsencrypt/live/kvartirabezvznosa.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kvartirabezvznosa.ru/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        proxy_pass https://s3.cloud.ru/kvartirabezvznosa/static/;
        proxy_set_header Host s3.cloud.ru;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Шаг 2. Запуск контейнеров и получение сертификатов

1. **Запусти контейнеры:**

   Из корня проекта выполни:

   ```bash
   sudo docker-compose up -d --build
   ```

2. **Проверь статус контейнеров:**

   ```bash
   sudo docker ps
   ```

   Убедись, что все контейнеры запущены.

3. **Получение сертификатов:**

   Контейнер `letsencrypt` автоматически обнаружит переменные `VIRTUAL_HOST` и `LETSENCRYPT_HOST` у сервиса `web` и начнет процесс получения сертификатов для указанных доменов.  
   Для проверки можно посмотреть логи:

   ```bash
   sudo docker logs nginx_letsencrypt
   ```

   В логах должны появиться сообщения об успешной регистрации аккаунта, верификации доменов, получении сертификатов и установке их в том `certbot_certs`.

4. **Проверка сертификатов в nginx‑proxy:**

   Выполни в контейнере `nginx_proxy` команду:

   ```bash
   sudo docker exec -it nginx_proxy ls -l /etc/nginx/certs
   ```

   Ты должен увидеть символические ссылки на сертификаты для каждого домена (например, для `kvartirabezvznosa.ru`).

---

## Шаг 3. Настройка автоматического продления сертификатов

Контейнер `letsencrypt` (companion) периодически проверяет состояние сертификатов. Переменная `LETSENCRYPT_REFRESH_INTERVAL=3600` означает, что companion проверяет сертификаты каждый час.  
Когда до истечения срока действия сертификата останется менее 30 дней, companion автоматически инициирует процесс продления.

Проверить работу автоматического продления можно следующим образом:

1. Просмотр логов контейнера:

   ```bash
   sudo docker logs nginx_letsencrypt
   ```

   В логах будут появляться сообщения о проверке и, при необходимости, о продлении сертификатов.

2. В продакшене интервал проверки обычно оставляют равным 3600 секунд (1 час), чтобы не перегружать систему лишними запросами к API Let’s Encrypt.

---

## Шаг 4. Доступ к сайту по HTTPS

1. Открой браузер и перейди по адресу, например:

   ```
   https://kvartirabezvznosa.ru
   ```

2. Проверь, что соединение защищено (в браузере появится зеленый замок, сертификат валиден).

3. Если сертификат отображается корректно, а сайт работает – установка SSL завершена.

---

## Резюме

- **Dockerfile**: собирает контейнер с Django‑приложением, работающим на Gunicorn (порт 8000).
- **docker-compose.yml**: содержит сервисы `nginx-proxy`, `letsencrypt` и `web`. Переменные окружения (VIRTUAL_HOST, LETSENCRYPT_HOST, LETSENCRYPT_EMAIL, VIRTUAL_PORT) позволяют автоматически получить и установить сертификаты для указанных доменов.
- **Конфигурация Nginx**: обрабатывает HTTP, редиректит на HTTPS и проксирует запросы к Django‑приложению.
- **Автоматическое продление**: companion проверяет сертификаты каждый час и продлевает их, когда до окончания срока действия остаётся менее 30 дней.

Эта инструкция описывает весь процесс – от подготовки файлов до получения, установки и автоматического продления SSL‑сертификатов для веб‑приложения Django, размещённого в Docker‑контейнерах.

---

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

### Инструкция по установке

1. Зарегистрируйтесь в Cloud.ru и создайте сервер VPS. Подключитесь к VPS серверу по SSH через публичный ключ. Для подключения используйте VSCod.
2. Зарегистрируйтесь в GitHub и создайте пустой без каких либо файлов публичный репозиторий.
3. На локальном ПК создайте папку, которая должна называться также, как ваш репозиторий GitHub. Клонируйте репозиторий с кодом веб приложения на локальный компьютер.
```
git clone https://github.com/myasoedas/kvartirabezvznosa.ru.git .
```
Точка на конце позволяет клонировать код без создания папки.
4. Отвяжите клонированный репозиторий на локальной машине от удаленного репозитория в GitHub.
5. Привяжите клонированный репозиторий на локальной машине к вашему новому пустому публичного репозиторию на GitHub.
6. На локальном ПК сгенерируйте публичный и приватный ключи для доступа через SSH.
7. Настройте удаленный доступ вашего нового репозитория к серверу VPS по SSH через публичный ключ. В настройки вашего репозитория загрузите приватный ключ, в настройки SSH вашего сервера VPS загрузите публичный ключ.
8. Настройте доступ по SSH к вашему GitHub. Добавьте публичный ключ в глобальные настройки вашего аккаунта GitHub. Добавьте в секреты репозиторя все необходимые для работы веб приложения переменные окружения из файла .env.
9. Схема работы: на локальном ПК пищете код, через git push отправляете изменения кода на локальном ПК в удаленный репозиторий GitHub, где запускается скрипт GitHub Actions который автоматически обновляет код на сервере VPS и выполняет деплой веб приложения в докер контейнерах.
10. Перед тем как выполнить первый деплой на сервере VPS необходимо создать бакет s3 хранилище на Cloud.ru. Создайте папки static и media.
11. На локальном ПК установите клиент awscli, который работает в командной строке, отредактируйте его конфиги чтобы он получил доступ к управлению бакетом в Cloud.ru с локального ПК.
12. Через клиент awscli загрузите политики для бакета относительно папок static и media, чтобы они стали доступными по ссылке.
13. Запишите в конфиги на локальном ПК настройки подключения к бакетам.