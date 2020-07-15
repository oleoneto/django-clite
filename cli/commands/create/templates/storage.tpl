from storages.backends.s3boto3 import S3Boto3Storage

# Static assets: CSS, Javascript
class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True


class PrivateFileStorage(S3Boto3Storage):
    location = 'private-files'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class PublicFileStorage(S3Boto3Storage):
    location = 'files'
    default_acl = 'public-read'
    file_overwrite = False
