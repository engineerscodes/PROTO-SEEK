from django.db import models

# Create your models here.
from django.db import models

from Teacher.models import TeacherClassRoom
# Create your models here.

class Event(models.Model):
    class Meta:
        unique_together = (('eventname', 'Room'))
    eventname = models.CharField(max_length=50)
    Room=models.ForeignKey(TeacherClassRoom,on_delete=models.CASCADE)

    def __str__(self):
        return "Room :"+self.Room.classRoomName+"| Event :"+self.eventname