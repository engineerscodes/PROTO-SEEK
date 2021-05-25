from django.contrib import admin
from .models import Mode
# Register your models here.
class ModelDetails(admin.ModelAdmin):
    list_display = ('email','username','mode_active')
    search_fields = ('email','username')
    list_filter = ('email','username','mode_active')

admin.site.register(Mode,ModelDetails)