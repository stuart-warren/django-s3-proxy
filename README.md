django-s3-proxy
===============

Playing with proxying requests to an S3 bucket

requires:
https://github.com/stuart-warren/django-boto

Currently pretty basic.

Create a local_settings.py:

```
AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
BOTO_S3_HOST = 'objects.dreamhost.com'
AWS_ACL_POLICY = 'private'
```

Do the usual ``python manage.py syncdb`` and create a root user.

Start up the dev server ``python manage.py runserver``

Add a bucket and some objects through the admin interface. ``http://127.0.0.1:8000/admin/``

Ensure they have been created in the actual s3 buckets.

go to ``http://127.0.0.1:8000/proxy/name_of_bucket/path/of/key``

You should see or be prompted to download the file...

Essentially this subverts the privateness of your s3 buckets for objects you have created, but we could now implement our own security for individual buckets. LDAP for example.

Also I intend to index each file created into elasticsearch using Haystack for searchable s3 buckets.

Plus allow ``PUT``ting files to a key to create them rather than through the interface (would require basic auth) in order to work with maven (Java)
