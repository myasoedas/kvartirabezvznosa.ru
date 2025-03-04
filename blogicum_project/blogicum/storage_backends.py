from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from botocore.client import Config


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    file_overwrite = True
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def connection_params(self):
        params = super().connection_params() or {}
        params.update({"config": Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION)})
        return params


class MediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def connection_params(self):
        params = super().connection_params() or {}
        params.update({"config": Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION)})
        return params
