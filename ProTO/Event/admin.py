from django.contrib import admin
from .models import Event
# Register your models here.

class AdminEvents(admin.ModelAdmin):
    list_display = ('eventname',)
    search_fields = ('eventname',)
    list_filter = ('eventname',)


admin.site.register(Event,AdminEvents)