from django.db import models
from django.conf import settings
from django.core.validators import validate_slug, RegexValidator
from django_boto.s3 import upload, remove, get_url
from django.core.files.base import ContentFile
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
    last_updated = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.fileObj = ContentFile(self.content)
        upload(self.fileObj,
                 name=self.key,
                 bucket_name=self.bucket.name,
                 key=settings.AWS_ACCESS_KEY_ID,
                 secret=settings.AWS_SECRET_ACCESS_KEY,
                 host=settings.BOTO_S3_HOST,
                 expires=0,
                 query_auth=True)
        super(S3Object, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        remove(name=self.key,
               bucket_name=self.bucket.name,
               key=settings.AWS_ACCESS_KEY_ID,
               secret=settings.AWS_SECRET_ACCESS_KEY,
               host=settings.BOTO_S3_HOST)
        super(S3Object, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return get_url(name=self.key,
                       bucket_name=self.bucket.name,
                       key=settings.AWS_ACCESS_KEY_ID,
                       secret=settings.AWS_SECRET_ACCESS_KEY,
                       host=settings.BOTO_S3_HOST,
                       query_auth=True)
