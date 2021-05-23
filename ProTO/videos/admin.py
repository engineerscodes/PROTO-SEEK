from django.contrib import admin
from .models import videoUpload,Marks
# Register your models here.

class adminvideoDetails(admin.ModelAdmin):
    list_display=('username','Total_marks','date','EventName')
    search_fields = ('username','date','captions','EventName')
    list_filter = ('username','date','EventName')
    exclude = ('thumbnail',)
    readonly_fields =('username','url_64encoding','Total_marks','EventName')

class MarksDetails(admin.ModelAdmin):
    list_display = ('videoId','by_email','marks','moderator_email','date','EventName')
    search_fields = ('videoId','by_email','marks','moderator_email','date','EventName')
    list_filter = ('by_email','moderator_email','date','videoId','EventName')
    readonly_fields = ('marks','video_link','videoId','moderator_email','by_email','EventName')

admin.site.register(videoUpload,adminvideoDetails)
admin.site.register(Marks,MarksDetails)