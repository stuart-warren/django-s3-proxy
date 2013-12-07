from django.db import models
from django.core.validators import validate_slug, RegexValidator
from storages.backends.s3boto import S3BotoStorage
import re

validate_path = RegexValidator(re.compile(r'^/[-a-zA-Z0-9_/.]+$'),
                    ("Enter a valid 'path' consisting of letters, "
                     "numbers, slashes, periods, underscores or hyphens. "
                     "Must start with /"))


class Bucket(models.Model):
    name = models.CharField(max_length=100, primary_key=True, validators=[validate_slug])
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=100)
    comment = models.CharField(max_length=500, blank=True)
    put_once = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class S3Object(models.Model):
    bucket = models.ForeignKey(Bucket)
    key = models.CharField(max_length=1024, validators=[validate_path], primary_key=True)
    content = models.FileField(storage=S3BotoStorage(
                                        acl='private',
                                        querystring_auth=True,
                                        querystring_expire=120,
                                        bucket_name=bucket.name,
                                        auto_create_bucket=True
                                       ),
                                upload_to=lambda instance, filename: instance.key
                                )

    def __unicode__(self):
        return self.key
