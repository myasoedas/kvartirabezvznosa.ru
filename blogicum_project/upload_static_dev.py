import os
import boto3
import mimetypes

from botocore.client import Config  # Импорт Config из botocore
from decouple import config
from pathlib import Path


# 🔹 Конфигурация S3
AWS_TENANT_ID = config('AWS_TENANT_ID')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_BUCKET_NAME = config('AWS_S3_SIGNATURE_VERSION')

# 🔹 Создаем клиента S3 с дополнительными параметрами для новой версии boto3
session = boto3.session.Session()
s3 = session.client(
    "s3",
    aws_access_key_id=f"{AWS_TENANT_ID}:{AWS_ACCESS_KEY_ID}",  # Формат tenant_id:key_id
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=AWS_S3_ENDPOINT_URL,
    region_name=AWS_S3_REGION_NAME,
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "path"},  # Используем path-style addressing
        request_checksum_calculation='when_required', 
        response_checksum_validation='when_required',
    )
)

# 🔹 Проверяем соединение
try:
    response = s3.list_buckets()
    print("✅ Доступные бакеты:", [bucket["Name"] for bucket in response["Buckets"]])
except Exception as e:
    print("🛑 Ошибка подключения к S3:", e)
    exit(1)

# 🔹 Папка с локальной статикой и префикс в бакете
LOCAL_STATIC_DIR = "static_dev"
S3_STATIC_PREFIX = "static"

print(f"🚀 Начинаем загрузку файлов из '{LOCAL_STATIC_DIR}' в S3 бакет '{AWS_BUCKET_NAME}/{S3_STATIC_PREFIX}'")

# 🔹 Проверяем, существует ли папка с локальной статикой
if not os.path.exists(LOCAL_STATIC_DIR):
    print(f"🛑 Ошибка: Папка '{LOCAL_STATIC_DIR}' не найдена!")
    exit(1)

# 🔹 Функция для определения MIME-типа файла
def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type if mime_type else "application/octet-stream"

# 🔹 Обходим файлы и загружаем их в S3, используя метод upload_file,
# который автоматически определяет размер файла и устанавливает Content-Length.
for root, _, files in os.walk(LOCAL_STATIC_DIR):
    for file_name in files:
        local_path = os.path.join(root, file_name)  # Полный путь к файлу
        s3_path = os.path.relpath(local_path, LOCAL_STATIC_DIR)  # Относительный путь
        s3_key = f"{S3_STATIC_PREFIX}/{s3_path}"  # Путь в бакете

        try:
            s3.upload_file(
                local_path,
                AWS_BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    "ContentType": get_mime_type(local_path),  # Автоопределение MIME-типа
                    "CacheControl": "max-age=86400",
                }
            )
            print(f"✅ Успешно загружен: {s3_key}")
        except Exception as e:
            print(f"🛑 Ошибка загрузки {s3_key}: {e}")

print("🎉 Загрузка завершена!")