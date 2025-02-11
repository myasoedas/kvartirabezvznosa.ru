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

## Шаг 2. Настройка файла docker-compose.yml

Используй следующий обновлённый вариант `docker-compose.yml` (он соответствует твоим рабочим файлам):

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
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
      - ./nginx/vhost.d:/etc/nginx/vhost.d:rw
      - ./nginx/html:/usr/share/nginx/html:rw
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
      - LETSENCRYPT_EMAIL=your_email@example.com
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

1. **Перейди в корень проекта** (где находится docker-compose.yml).  
2. **Собери и запусти контейнеры** командой:

   ```bash
   docker-compose up -d
   ```

   Контейнеры:
   - **nginx-proxy** будет слушать порты 80 и 443.
   - **letsencrypt** автоматически обнаружит контейнер web (на основе переменных VIRTUAL_HOST и LETSENCRYPT_HOST) и запросит сертификат для всех указанных доменов.
   - **web** запустит твое Django‑приложение через Gunicorn.
   - **db** запустит PostgreSQL.

---

## Шаг 5. Проверка выдачи сертификатов

1. **Проверь логи контейнера letsencrypt:**

   ```bash
   docker-compose logs letsencrypt
   ```

   В логах должно быть сообщение о том, что сертификат успешно получен и сохранён (путь, например, `/etc/letsencrypt/live/kvartirabezvznosa.ru/fullchain.pem`).

2. **Открой в браузере** любой из доменов (например, https://kvartirabezvznosa.ru) и убедись, что сайт доступен по HTTPS, а сертификат действителен.

---

## Шаг 6. Автоматическое обновление сертификатов

Контейнер **letsencrypt** автоматически продлевает сертификаты (обычно за 30 дней до истечения).  
Убедись, что:
- Именованный volume `certbot_certs` сохраняется между перезапусками контейнеров.
- Папки `./certbot/conf` и `./certbot/www` корректно смонтированы (как указано в docker-compose.yml).

Если потребуется принудительное обновление, можно выполнить:

```bash
docker-compose exec letsencrypt certbot renew --dry-run
```

Это позволит проверить, что процесс обновления работает без ошибок.

---

## Итоговая последовательность действий

1. **DNS:** Настроить A‑записи для всех доменов, указывающие на твой сервер.
2. **Структура проекта:** В корне проекта создать папки:
   - `/path/to/kvartirabezvznosa.ru/certbot/conf`
   - `/path/to/kvartirabezvznosa.ru/certbot/www`
   
   а также иметь каталоги `nginx/conf.d`, `nginx/vhost.d` и `nginx/html`.
3. **docker-compose.yml:** Использовать приведённый файл, в котором контейнеры nginx‑proxy, letsencrypt и web настроены для автоматической выдачи сертификата.
4. **nginx конфигурация:** Файл `nginx/conf.d/default.conf` должен содержать блоки для обработки ACME‑challenge и для HTTPS с сертификатами.
5. **Запуск:** Из корня проекта выполнить `docker-compose up -d`.
6. **Проверка:** Убедиться в успешном получении сертификата через логи letsencrypt и открыть домены в браузере.
7. **Обновление:** Контейнер letsencrypt автоматически продлевает сертификаты; можно проверить процесс через `certbot renew --dry-run`.

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

