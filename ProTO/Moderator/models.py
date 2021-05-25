from django.db import models

# Create your models here.

class Mode(models.Model):
     email=models.CharField(max_length=250,unique=True)
     mode_active=models.BooleanField(default=False)
     username=models.CharField(max_length=250,default='',unique=True)
     def __str__(self):
        return self.email +" is active :"+str(self.mode_active)