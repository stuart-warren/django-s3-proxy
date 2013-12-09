from django.contrib import admin
from proxy.models import Bucket, S3Object
# Register your models here.


# override the bulk delete to actually remove remote files
def delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()
delete_selected.short_description = 'Delete selected objects'


class BucketAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'allow_file_replace', 'comment', 'last_updated')
    list_filter = ['owner']
    search_fields = ['name', 'comment']


class S3ObjectAdmin(admin.ModelAdmin):
    list_display = ('key', 'bucket', 'last_updated')
    list_filter = ['bucket']
    search_fields = ['key']
    actions = [delete_selected]

admin.site.register(Bucket, BucketAdmin)
admin.site.register(S3Object, S3ObjectAdmin)
