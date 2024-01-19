from django.conf import settings 
from storages.backends.s3boto3 import S3Boto3Storage

# THIS IS CREATED TO ALLOW STATIC AND MEDIA FILES TO BE DIRECTLY UPLOADED TO S3
class StaticFileStorage(S3Boto3Storage):
    location = settings.STATICFILES_FOLDER # overwriting the location attr for this class

class MediaFileStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_FOLDER