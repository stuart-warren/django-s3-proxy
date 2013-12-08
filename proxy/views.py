from django.shortcuts import render, get_object_or_404
from django import http
from django.http import HttpResponse
from django_boto.s3 import get_url
from django.conf import settings
# Create your views here.
from proxy.models import Bucket, S3Object


def search(request):
    return HttpResponse("Put search here!")


def get(request, bucket_name, key):
    bucket = get_object_or_404(Bucket, pk=bucket_name)
    s3object = get_object_or_404(S3Object, pk=key)
    url = get_url(name=s3object.key,
                   bucket_name=s3object.bucket.name,
                   key=settings.AWS_ACCESS_KEY_ID,
                   secret=settings.AWS_SECRET_ACCESS_KEY,
                   host=settings.BOTO_S3_HOST,
                   query_auth=True)
    # return render(request, 'proxy/test.html', {'bucket': bucket, 'request': request, 'key': key, 'url': url})
    return http.HttpResponseRedirect(url)
