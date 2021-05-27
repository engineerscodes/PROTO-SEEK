from django.db import models
from .VideoSizeVal import file_size
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from Event.models import Event

class videoUpload(models.Model):

    captions=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    date=models.DateField(default='2001-04-12')
    EventName=models.CharField(max_length=50,default="")
    thumbnail=models.TextField()
    video=models.FileField(upload_to="videos/%y",validators=[file_size,FileExtensionValidator(allowed_extensions=['mp4','MOV','MKV'])])
    url_64encoding=models.CharField(max_length=2048,default='/upload/videos/')
    Total_marks=models.IntegerField(default=0)
    EventID=models.CharField(max_length=100,default='welcome newbie')
    def __str__(self):
        return  self.captions
    def total_marks(self):
        return self.Total_marks


class Marks(models.Model):
    class Meta:
        unique_together=(('videoId','moderator_email'))
    videoId=models.CharField(max_length=250)
    by_email=models.CharField(max_length=250)
    marks=models.IntegerField(validators=[MinValueValidator(0)])
    moderator_email=models.CharField(max_length=250)
    video_link=models.CharField(max_length=100000)
    date=models.DateField(default='2001-04-12')
    EventName = models.CharField(max_length=50, default="")
    verfiyed=models.BooleanField(default=False)
    def __str__(self):
        return "VideoID:" +self.video_link+" BY :"+self.moderator_email
