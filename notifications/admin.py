from django.contrib import admin
from .models import NotificationPost
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title','date',]
    list_per_number = 50
    list_filter = ['title','date',]
    search_fields = ['title','date']

admin.site.register(NotificationPost, NotificationAdmin)