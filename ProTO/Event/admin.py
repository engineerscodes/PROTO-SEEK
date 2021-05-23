from django.contrib import admin
from .models import Event
# Register your models here.

class AdminEvents(admin.ModelAdmin):
    list_display = ('eventname','Room','id')
    search_fields = ('eventname','Room')
    list_filter = ('eventname','Room','id')


admin.site.register(Event,AdminEvents)