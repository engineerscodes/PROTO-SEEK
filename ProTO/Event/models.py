from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class Event(models.Model):

    eventname = models.CharField(max_length=50)

    def __str__(self):
        return self.eventname