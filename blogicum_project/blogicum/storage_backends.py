from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from botocore.client import Config

class StaticStorage(S3Boto3Storage):
    # Файлы статики будут храниться в бакете в папке "static"
    location = 'static'
    # Делает файлы доступными для чтения без аутентификации         
    default_acl = 'public-read'   
    file_overwrite = True

    def connection_params(self):
        """
        Переопределяем метод для добавления дополнительных параметров в конфигурацию boto3.
        """
        params = super().connection_params() or {}
        params.update({"config": Config(**settings.AWS_S3_CONFIG)})
        return params
