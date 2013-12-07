from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from proxy.models import Bucket, S3Object


def search(request):
    return HttpResponse("Put search here!")


def index(request, bucket_name, key):
    #bucket = ''
    bucket = get_object_or_404(Bucket, pk=bucket_name)
    #s3object = ''
    s3object = get_object_or_404(S3Object, pk=key)
    return render(request, 'proxy/test.html', {'bucket': bucket, 'request': request, 'key': key, 's3object': s3object})
