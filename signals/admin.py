from django.contrib import admin
from .models import Signals
# Register your models here.


class SignalAdmin(admin.ModelAdmin):
    list_display = ['title','Buy','TP','SL','publisheddate']
    list_per_number = 50
    list_filter = ['title','Buy','TP','SL', 'publisheddate']
    search_fields = ['title','Buy','TP','SL', 'publisheddate']
 
admin.site.register(Signals, SignalAdmin)