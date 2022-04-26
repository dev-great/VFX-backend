from django.contrib import admin
from .models import FeedPost
# Register your models here.

class FeedAdmin(admin.ModelAdmin):
    list_per_number = 50
    list_filter = ['publisheddate']
    search_fields = ['publisheddate']

admin.site.register(FeedPost, FeedAdmin)