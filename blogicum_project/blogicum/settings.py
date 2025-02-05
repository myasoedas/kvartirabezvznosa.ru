import os
from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

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
# https://s3.cloud.ru/bucket-violetta/static/...
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
